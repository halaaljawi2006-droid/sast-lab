import sqlite3
import subprocess
import hashlib
import pickle

from flask import Flask, request

app = Flask(__name__)

DB_PASSWORD = "admin123"  # Hardcoded password


@app.route("/user")
def get_user():
    username = request.args.get("name")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SQL Injection
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return str(cursor.fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host")
    # Command Injection
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return output


@app.route("/calc")
def calc():
    expr = request.args.get("expr")
    # Code Injection
    return str(eval(expr))


@app.route("/load")
def load():
    data = request.get_data()
    # Insecure deserialization
    return str(pickle.loads(data))


def hash_password(password):
    # Weak hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()


if __name__ == "__main__":
    # Debug mode enabled in production
    app.run(debug=True)
