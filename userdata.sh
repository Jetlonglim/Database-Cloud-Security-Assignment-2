#!/bin/bash
set -euxo pipefail

dnf update -y
dnf install -y python3 pip

mkdir -p /opt/libraryapp
cat > /opt/libraryapp/app.py <<'PY'
from flask import Flask, request
app = Flask(__name__)

@app.get("/")
def home():
    return "Library Management System - OK"

@app.get("/search")
def search():
    q = request.args.get("q","")
    # We intentionally treat user input as plain string to demonstrate safe handling.
    return f"Search query received safely: {q}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
PY

pip3 install flask

cat > /etc/systemd/system/libraryapp.service <<'SERVICE'
[Unit]
Description=Library Flask App
After=network.target

[Service]
WorkingDirectory=/opt/libraryapp
ExecStart=/usr/bin/python3 /opt/libraryapp/app.py
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable libraryapp
systemctl start libraryapp
