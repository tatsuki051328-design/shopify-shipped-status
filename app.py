from flask import Flask, request
from workflow import handle_order_shipped

app = Flask(__name__)

@app.route("/")
def index():
    return "ok"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    customer_gid = data["customer"]["admin_graphql_api_id"]
    handle_order_shipped(customer_gid)
    print(customer_gid)
    return {"status": "received"}

