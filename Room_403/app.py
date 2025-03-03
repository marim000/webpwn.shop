from flask import Flask, request, abort, render_template, send_file

app = Flask(__name__)

ALLOWED_HEADERS = [
    'X-Forwarded-For', 'X-Original-URL', 'X-Rewrite-URL', 'X-Originating-IP',
    'X-Remote-IP', 'X-Remote-Addr', 'X-Forwarded', 'X-Client-IP', 
    'X-Bypass-Header', 'X-Real-IP', 'True-Client-IP', 'Forwarded-For', 'Client-IP'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visitor_list.txt')
def list():
    forbidden_patterns = ['%2F', '%252F', '%2e', '../', '..%2F', '..%252F', '..%5C', '..%255C', '%5C', '%255C']
    if any(pattern in request.url for pattern in forbidden_patterns):
        return render_template('deny.html')

    for header in ALLOWED_HEADERS:
        if header in request.headers:
             return send_file('visitor_list.txt')

    abort(403)

if __name__ == '__main__':
    app.run(debug=True)
