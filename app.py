from flask import Flask, request, jsonify, make_response, redirect
import os
import sqlite3
import jwt
import subprocess

app = Flask(__name__)

SECRET_KEY = "123456"

def init_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'password123')")
    conn.commit()
    conn.close()

init_db()

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        response = make_response(jsonify({"message": "Login successful", "user": username}))
        response.set_cookie("session", f"{username}:auth-token", httponly=False, secure=False)
        return response
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/admin-backdoor", methods=["GET"])
def admin_backdoor():
    token = request.headers.get("Authorization")
    if token == "supersecrettoken":
        return jsonify({"message": "Welcome, Admin!"})
    return jsonify({"message": "Access Denied"}), 403

@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify({"users": users})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    upload_path = os.path.join("uploads", file.filename)
    file.save(upload_path)

    return jsonify({"message": f"File {file.filename} uploaded successfully"})

@app.route("/jwt-auth", methods=["POST"])
def jwt_auth():
    username = request.form.get("username")
    token = jwt.encode({"user": username}, SECRET_KEY, algorithm="none")

    return jsonify({"token": token})

@app.route("/unsafe-redirect", methods=["GET"])
def unsafe_redirect():
    url = request.args.get("url")
    return redirect(url)

@app.route("/xss", methods=["GET", "POST"])
def xss():
    user_input = request.args.get("input", "")
    return f"<html><body><h1>{user_input}</h1></body></html>"

@app.route("/cmd-injection", methods=["POST"])
def cmd_injection():
    command = request.form.get("command")
    output = subprocess.check_output(command, shell=True)
    return jsonify({"output": output.decode()})

if __name__ == "__main__":
    app.run(debug=True)

