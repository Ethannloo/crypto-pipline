from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
from sqlalchemy import create_engine


def fetch_and_store_crypto_data():
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
        engine = create_engine('postgresql://postgres:2004@host.docker.internal:5432/crypto_data')

        # Load data into PostgreSQL
        df.to_sql('crypto_prices', engine, if_exists='append', index=False)

    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


default_args = {
    'owner': 'Ethan',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes = 5),
}

with DAG(
    'crypto_pipeline',
    default_args=default_args,
    description='A simple ETL pipeline to fetch and load crypto prices',
    schedule_interval='@daily',  # This will run the DAG once a day
    catchup = False,
) as dag:

    fetch_and_store_task = PythonOperator(
        task_id = 'fetch_and_store_crypto',
        python_callable = fetch_and_store_crypto_data,
    )

    fetch_and_store_task
