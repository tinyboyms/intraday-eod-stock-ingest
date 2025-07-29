# fetch_data.py
import requests
import pandas as pd
from config import API_URL, ACCESS_KEY

def fetch_stock_data():
    headers = {
        'Authorization': f'Bearer {ACCESS_KEY}'  # Or 'Token {ACCESS_KEY}', depends on API spec
    }
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    json_data = response.json()

    raw_data = json_data.get('data', [])
    df = pd.DataFrame(raw_data)

    return df
