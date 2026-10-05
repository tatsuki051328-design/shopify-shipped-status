from notion_api import get_data_source_id, query_orders_db, update_status_property, query_stock_db, get_billing_name
import os
from dotenv import load_dotenv
load_dotenv()

ORDERS_DB_ID = os.environ["ORDERS_DB_ID"]
STOCK_DB_ID = os.environ["STOCK_DB_ID"]

def handle_order_shipped(customer_gid):
    data_source_id = get_data_source_id(ORDERS_DB_ID)
    stock_data_source_id = get_data_source_id(STOCK_DB_ID)
    orders = query_orders_db(data_source_id, customer_gid)

    for order in orders:
        order_id = order["id"]
        update_status_property(order_id, "発送済み")
        billing_name = get_billing_name(order)
        if not billing_name:
            continue
        stocks = query_stock_db(stock_data_source_id, billing_name)
        for stock in stocks:
            stock_id = stock["id"]
            update_status_property(stock_id, "Archive")

if __name__ == "__main__":
    handle_order_shipped("gid://shopify/Customer/9566610292905")