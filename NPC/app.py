import sqlite3
from flask import Flask, render_template, request, jsonify, send_file
from lxml import etree
import pandas as pd
import io
from html import escape


app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

PRODUCTS = [
    {"id": 1, "model": "[Season]Winterboard", "description": "It is well aged because it is buried in the snow. It is eco-friendly with snow. It is a winter-only product, so you can't buy it now."},
    {"id": 2, "model": "[Best]Fallenleaves", "description": "Made a CPU out of leaves, so it's fairly lightweight and eco-friendly."},
    {"id": 3, "model": "[Sale]Wooden", "description": "Since it is made of wood, it burns quite well, so if you use it for a long time, it can cause a fire due to heat. However, it is eco-friendly. Refunds are not possible because it is on sale."}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

@app.route('/products')
def products():
    return render_template('products.html', products=PRODUCTS)

@app.route('/applicants')
def applicants():
    return render_template('applicants.html')

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    return "Product not found", 404

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_content = escape(request.form.get('feedback'))

    if feedback_content:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (content) VALUES (?)", (feedback_content,))
        conn.commit()
        conn.close()
        return "Feedback submitted successfully!"
    return "Invalid feedback content!", 400

@app.route('/download', methods=['POST'])
def download():
    if 'file' not in request.files:
        return "No file part", 400
    
    xml_file = request.files['file']
    
    if xml_file.filename == '':
        return "No selected file", 400
    
    xml_data = xml_file.read()
    
    xml_data = xml_data.decode('UTF-8')
    xml_data = xml_data.replace("SYSTEM", "system")
    xml_data = xml_data.encode('UTF-8')

    parser = etree.XMLParser(encoding='UTF-8')
    try:
        root = etree.fromstring(xml_data, parser=parser)
    except etree.XMLSyntaxError as e:
        print("XML Syntax Error:", e)
        return "Error parsing XML file", 400
    except Exception as e:
        print("Unexpected Error:", e)
        return "Unexpected error occurred", 500
    except:
        root = etree.fromstring("<name>fail</name>", parser=parser)

    data = []
    try:
        for applicant in root.findall('applicant'):
            name = applicant.find('name').text
            age = applicant.find('age').text
            department = applicant.find('department').text
            address = applicant.find('address').text
            pass_status = applicant.find('pass').text
            data.append([name, age, department, address, pass_status])
        
        df = pd.DataFrame(data, columns=['Name', 'Age', 'Department', 'Address', 'Pass Status'])
        
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
    except:
        output = str()

    return send_file(output, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', download_name='applicants.xlsx')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    
