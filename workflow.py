from notion_api import get_data_source_id, query_orders_db, update_status_property, query_stock_db, get_billing_name
import os
from dotenv import load_dotenv
load_dotenv()

ORDERS_DB_ID = os.environ["ORDERS_DB_ID"]
STOCK_DB_ID = os.environ["STOCK_DB_ID"]
NOTION_API_KEY = os.environ["NOTION_API_KEY"]

def update_status(customer_git):
    data_source_id = get_data_source_id(ORDERS_DB_ID)
    orders = query_orders_db(data_source_id, customer_git)
    for order in orders:
        page_id = order["id"]
        update_status_property(page_id, "発送済み")

if __name__ == "__main__":
    update_status("gid://shopify/Customer/9566610292905")