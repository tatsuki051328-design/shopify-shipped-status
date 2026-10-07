from flask import Flask, request
from workflow import handle_order_shipped

app = Flask(__name__)

@app.route("/")
def index():
    return "ok"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    customer = data.get("customer")
    if not customer:
        return {"status": "skipped"}
    customer_gid = customer["admin_graphql_api_id"]
    handle_order_shipped(customer_gid)
    return {"status": "received"}

