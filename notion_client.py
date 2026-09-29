import os 
import requests
from dotenv import load_dotenv
import json

load_dotenv()

NOTION_API_KEY = os.environ["NOTION_API_KEY"]

def get_data_source_id(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2025-09-03"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["data_sources"][0]["id"]

def query_orders_db(data_source_id, customer_gid):
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    headers = {
        # ここは get_data_source_id と同じ中身のはず
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2025-09-03"
    }
    payload = {
        "filter": {
            "and": [
                # 1つ目の条件: admin_graphql_api_id が customer_gid と一致
                {"property": "admin_graphql_api_id", "rich_text": {"equals": f"{customer_gid}"}},
                # 2つ目の条件: ステータス が "未着手" と一致
                  {"property": "ステータス", "status": {"equals": "未着手"}}
            ]
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["results"]

if __name__ == "__main__":
        print(get_data_source_id("bc723bd360fc82bdbff181c4cdf0d61b"))
        query_db = query_orders_db("dc623bd3-60fc-83eb-a677-0762172032ca", "gid://shopify/Customer/9566610292905")
        print(json.dumps(query_db, indent=2, ensure_ascii=False))