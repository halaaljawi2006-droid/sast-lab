import os
import sqlite3
import subprocess
import hashlib
import json
import ast
import re

from flask import Flask, request, abort

app = Flask(__name__)

DB_PASSWORD = os.environ.get("DB_PASSWORD")  # Read secret from environment


@app.route("/user")
def get_user():
    username = request.args.get("name")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Fixed: parameterized query
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    return str(cursor.fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    # Fixed: validate input and avoid shell=True
    if not re.fullmatch(r"[A-Za-z0-9.\-]+", host):
        abort(400)
    output = subprocess.check_output(["ping", "-c", "1", host])  # nosec B603
    return output


@app.route("/calc")
def calc():
    expr = request.args.get("expr")
    # Fixed: literal_eval only accepts safe literals
    return str(ast.literal_eval(expr))


@app.route("/load")
def load():
    # Fixed: JSON instead of pickle
    return str(json.loads(request.get_data()))


def hash_password(password):
    # Fixed: strong hashing with salt
    salt = os.urandom(16)
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()


if __name__ == "__main__":
    # Fixed: debug disabled
    app.run(debug=False)
