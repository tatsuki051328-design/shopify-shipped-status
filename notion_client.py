import os 
import requests
from dotenv import load_dotenv
import json

load_dotenv()

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2025-09-03"
}

def get_data_source_id(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data["data_sources"][0]["id"]

def query_orders_db(data_source_id, customer_gid):
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    payload = {
        "filter": {
            "and": [
                # 1つ目の条件: admin_graphql_api_id が customer_gid と一致
                {"property": "admin_graphql_api_id", "rich_text": {"equals": customer_gid}},
                # 2つ目の条件: ステータス が "未着手" と一致
                {"property": "ステータス", "status": {"equals": "未着手"}}
            ]
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["results"]

def update_status_property(page_id, status):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {"ステータス": {"status": {"name":status}}}
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["properties"]["ステータス"]["status"]["name"]

def query_stock_db(data_source_id, customer_name):
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    payload = {
        "filter": {
            "and": [
                {"property": "ステータス", "status": {"equals": "Stock"}},
                {"property": "顧客名", "title": {"equals": customer_name}}
            ]
        }
    
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["results"]

# def update_stock_status_to_archive(page_id,status):
#     url = f"https://api.notion.com/v1/pages/{page_id}"
#     payload = {
#         "properties": {"ステータス": {"status": {"name":status}}}
#     }
#     response = requests.patch(url, headers=HEADERS, json=payload)
#     response.raise_for_status()
#     return response.json()

if __name__ == "__main__":
        # print(get_data_source_id("bc723bd360fc82bdbff181c4cdf0d61b"))
        # print(get_data_source_id("64723bd360fc82a2b9aa0192f63fc7ad"))
        # query_db = query_orders_db("dc623bd3-60fc-83eb-a677-0762172032ca", "gid://shopify/Customer/9566610292905")
        # print(json.dumps(query_db, indent=2, ensure_ascii=False))
        update_result = update_status_property("3ea23bd3-60fc-8125-ac99-e9966c61ddc2","発送済み")
        print(json.dumps(update_result, indent=2, ensure_ascii=False))
        # stock_db = query_stock_db("5e023bd3-60fc-82ba-9642-07820ef2b1ac", "清水幹雄")
        # print(json.dumps(stock_db, indent=2, ensure_ascii=False))
        stock_update_result = update_status_property("3ec23bd3-60fc-80fa-a6a1-dbf3d601f22c","Archive")
        print(json.dumps(stock_update_result, indent=2, ensure_ascii=False))
