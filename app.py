from flask import Flask, request
from workflow import handle_order_shipped
from shopify_parser import is_valid_shopify_signature
from dotenv import load_dotenv
import os
load_dotenv()

SHOPIFY_WEBHOOK_SECRET = os.environ["SHOPIFY_WEBHOOK_SECRET"]

app = Flask(__name__)

@app.route("/")
def index():
    return "ok"

@app.route("/webhook", methods=["POST"])
def webhook():
    raw_body = request.get_data()
    signature = request.headers.get("X-Shopify-Hmac-Sha256")
    if not signature or not is_valid_shopify_signature(raw_body, signature, SHOPIFY_WEBHOOK_SECRET):
        return {"status": "unauthorized"}, 401
    data = request.get_json()
    customer = data.get("customer")
    if not customer:
        return {"status": "skipped"}
    customer_gid = customer["admin_graphql_api_id"]
    handle_order_shipped(customer_gid)
    return {"status": "received"}
