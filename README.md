# Crypto Price ETL Pipeline with Airflow & PostgreSQL

## Overview
An end-to-end data pipeline that extracts cryptocurrency price data using the CoinGecko API, transforms it with pandas, and loads it into PostgreSQL, orchestrated and scheduled using Apache Airflow (Docker).

## Key Technologies:
- Python (pandas, requests, SQLAlchemy)
- PostgreSQL
- Apache Airflow (Docker)
- REST API (CoinGecko)

## How It Works:
1. Extracts top 5 cryptocurrency prices from CoinGecko API.
2. Transforms data (formats timestamps, selects relevant fields).
3. Loads data into a PostgreSQL table `crypto_prices`.
4. Airflow DAG schedules the pipeline to run daily.

## How to Run:
1. Clone the repository.
2. Set up Docker and navigate to the repo folder.
3. Start Airflow with:
   ```bash
   docker-compose up -d
