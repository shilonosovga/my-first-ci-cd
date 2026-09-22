import hashlib
import ipaddress
import subprocess

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    user_id = request.args.get("id", "1")
    return f"<h1>Hello, user #{escape(user_id)}!</h1>"


@app.route("/checksum")
def checksum():
    data = request.args.get("data", "")
    return hashlib.sha256(data.encode()).hexdigest()


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    try:
        ipaddress.ip_address(host)
    except ValueError:
        return "Invalid IP address", 400

    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        check=False,
        timeout=5,
    )

    return f"<pre>{escape(result.stdout.decode())}</pre>"


if __name__ == "__main__":
    app.run(debug=False)
