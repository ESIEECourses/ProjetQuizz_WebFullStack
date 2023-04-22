from flask import Flask
from flask_cors import CORS
from flask import Flask, request
from jwt_utils import build_token
import hashlib

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    name = 'world'
    return f"Hello, {name}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    triedPassword = payload['password'].encode('UTF-8')
    hashedPassword = hashlib.md5(triedPassword).digest()
    
    if hashedPassword == b'\x91\xf4\x02\xdc\xc4\xb1\xb0\xe9O\xc1\xf9\xa5\x18^\xc3\xd8':
        return { "token": build_token()}, 200
    else:
        return 'Unauthorized', 401

if __name__ == "__main__":
    app.run()
