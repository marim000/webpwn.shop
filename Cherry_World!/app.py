from flask import Flask, render_template, request, jsonify, make_response
import jwt
import uuid
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

SECRET_KEY = "very_secret_key"
FLAG = "WP{**flag**}"

def generate_jwt(user_id, is_admin=False, alg="HS256"):

    payload = {
        "user_id": user_id,
        "is_admin": is_admin,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
    }
    if alg == "none":
        token = jwt.encode(payload, key=None, algorithm="none")
    else:
        token = jwt.encode(payload, key=SECRET_KEY, algorithm=alg)
    return token

def verify_jwt_token(token):
    try:
        header = jwt.get_unverified_header(token)
        
        if header.get("alg") == "none":
            decoded = jwt.decode(token, options={"verify_signature": False})
        else:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
@app.route('/')
def index():
    token = request.cookies.get('jwt_token')
    
    if token:
        response = make_response(render_template('index.html'))
        response.delete_cookie('jwt_token')
        
        user_id = str(uuid.uuid4())
        token = generate_jwt(user_id)
        
        response.set_cookie('jwt_token', token, httponly=True)
        return response

    user_id = str(uuid.uuid4())
    token = generate_jwt(user_id)

    response = make_response(render_template('index.html'))
    response.set_cookie('jwt_token', token, httponly=True)
    return response

@app.route('/guest')
def guest():
    user_id = request.cookies.get('jwt_token')
    if user_id:
        return render_template('guest.html')

@app.route('/admin')
def admin():
    token = request.cookies.get('jwt_token')
    if token:
        decoded = verify_jwt_token(token)
        if decoded:
            if decoded.get('is_admin', False):
                return render_template('admin.html', flag=FLAG)
            else:
                return render_template('error.html')
        else:
            return jsonify({'status': 'error', 'message': 'Invalid or expired token.'}), 401
    return jsonify({'status': 'error', 'message': 'No token provided.'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20005)
