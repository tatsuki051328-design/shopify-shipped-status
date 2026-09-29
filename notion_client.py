import os 
import requests
from dotenv import load_dotenv

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

if __name__ == "__main__":
        print(get_data_source_id("bc723bd360fc82bdbff181c4cdf0d61b"))