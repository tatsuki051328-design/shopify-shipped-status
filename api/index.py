from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "ok"

@app.route("/webhook", method=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    return {"status": "received"}

