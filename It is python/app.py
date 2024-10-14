from flask import Flask, session, render_template, request
import os, random, hashlib, subprocess

app = Flask(__name__)
app.secret_key = "*******"

@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    if 'mysession' not in session :
        rand_hash = hashlib.md5(('*******'+str(random.randint(0,999999))).encode('utf-8')).hexdigest()
        session['mysession'] = rand_hash

        os.makedirs('./sessions/'+session['mysession'])
        with open('./ccctf.py', 'r') as f:
            contents = f.read()
        with open('./sessions/'+session['mysession']+'/ccctf.py', 'w') as f:
            f.write(contents)
        with open('./flag.py', 'r') as f:
            contents = f.read()
        with open('./sessions/'+session['mysession']+'/flag.py', 'w') as f:
            f.write(contents)

    return 'WELCOME TO CCCTF'

    
@app.route("/write", methods=["GET"])
def write():
    file = request.args.get('file')
    data = request.args.get('data')

    if "../" in file :
        return "fail"
        
    with open('./sessions/'+session['mysession']+'/'+file, 'w') as f:
        f.write(data)
    
    return "success"


@app.route('/flag', methods=['GET'])
def flag():
    try:
        result = subprocess.run(args=["python3", './sessions/'+session['mysession']+'/ccctf.py'], capture_output=True, text=True)
        return result.stdout
    
    except:
        return "error"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12345)