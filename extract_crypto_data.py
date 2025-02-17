import requests
import pandas as pd
from sqlalchemy import create_engine

def fetch_and_store_crypto_data():
    # API Call
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1
    }
    response = requests.get(url, params = params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df = df[['id', 'symbol', 'current_price', 'market_cap', 'last_updated']]
        df['last_updated'] = pd.to_datetime(df['last_updated'])

        # Connect to PostgreSQL
        engine = create_engine('postgresql://postgres:2004@localhost:5432/crypto_data')

        # Write data to PostgreSQL
        df.to_sql('crypto_prices', engine, if_exists='append', index=False)
        print("Data inserted successfully!")

    else:
        print("Failed to fetch data:", response.status_code)

if __name__ == '__main__':
    fetch_and_store_crypto_data()
