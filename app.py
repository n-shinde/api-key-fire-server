# Run in terminal to install dependencies
# pip install -r requirements.txt

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

with open('users.json') as f:
    users = json.load(f)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if users.get(username) == password:
        session["user"] = username
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/get-api-key', methods=['GET'])
def get_api_key():
    if "user" in session:
        return jsonify({"api_key": os.getenv("API_KEY")})
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/logout')
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)