# Run in terminal to install dependencies
# pip install -r requirements.txt

from flask import Flask, request, jsonify, session, render_template_string
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# HTML template for login form
login_form_html = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    <form method="POST" action="/login-form">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(login_form_html)

# Route to handle form-based login
@app.route('/login-form', methods=['POST'])
def login_form():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["user"] = username
        return f"Welcome, {username}! <br><br><a href='/get-api-key'>Get API Key</a> | <a href='/logout'>Logout</a>"
    
    return "Invalid credentials. <a href='/'>Try again</a>"

# API route to handle programmatic login (JSON format)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["user"] = username
        return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

# Route to get API key (show once per session)
@app.route('/get-api-key', methods=['GET'])
def get_api_key():
    if "user" in session and session["user"] == ADMIN_USERNAME:
        if session.get("api_key_shown"):
            return "API key has already been retrieved this session. <br><br><a href='/logout'>Logout</a>", 403
        
        session["api_key_shown"] = True
        api_key = os.getenv("API_KEY")

        return render_template_string(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Your API Key</title>
            <script>
                function copyToClipboard() {{
                    var copyText = document.getElementById("api-key");
                    navigator.clipboard.writeText(copyText.textContent).then(function() {{
                        alert("Copied to clipboard!");
                    }});
                }}
            </script>
        </head>
        <body>
            <h2>Your API Key</h2>
            <p id="api-key" style="font-weight: bold;">{api_key}</p>
            <button onclick="copyToClipboard()">Copy API Key</button><br><br>
            <a href='/logout'>Logout</a>
        </body>
        </html>
        """)
    
    return "Unauthorized access. <a href='/'>Login</a>", 401

# Route to logout and reset session
@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("api_key_shown", None)  # Reset key visibility flag
    return "Logged out. <a href='/'>Go back</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)