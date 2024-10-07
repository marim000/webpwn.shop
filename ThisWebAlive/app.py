from flask import Flask, request, render_template
import re, subprocess

app = Flask(__name__)

@app.route('/' , methods=['GET'])
def index():
    host = request.args.get('host','')

    if not host:
        return render_template('index.html')
    
    if re.search(r'[;&|\\$()<>`{}]', host):
        return 'Don\'t try attack! :('

    cmd = f'ping {host} -c 1'
    try:
        subprocess.check_output(['/bin/sh', '-c', cmd], timeout=5)
        return 'Alive!'
    except subprocess.TimeoutExpired:
        return 'Timeout'
    except subprocess.CalledProcessError:
        return 'Error'

app.run(host='0.0.0.0', port=8000)
