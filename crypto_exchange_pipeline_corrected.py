import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

# Google Cloud Configuration
GCP_PROJECT = "learn-airflow-428415"
GCS_BUCKET = "crypto-exchange-pipeline-priyadarshigupta"
GCS_RAW_DATA_PATH = "raw_data/crypto_raw_data"
GCS_TRANSFORMED_DATA_PATH = "transformed_data/crypto_raw_data"
GCS_TRANSFORMED_OUTPUT_PATH = "transformed_data/crypto_transformed_data"

# Function to fetch crypto market data
def fetch_api_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': "usd",
        'order': 'market_cap_desc',
        'per_page': 10,
        'sparkline': False
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(data)

    with open("crypto_data.json", "w") as f:
        json.dump(data, f, indent=4)


def transform_data():
    with open("crypto_data.json", "r") as f:
        data=json.load(data,f)

    transformed_data=[]
    for item in data:
        transformed_data.append({
            'id': item['id'],
            'name': item['name'],
            'symbol': item['symbol'],
            'current_price': item['current_price'],
            'market_cap': item['market_cap'],
            'market_cap_desc': item['market_cap_desc'],
            'total_volume': item['total_volume'],
            'total_volume_desc': item['total_volume_desc'],
            'timestamp': item['timestamp'],
            'last_updated': item['last_updated'],
            'timestamp_desc': datetime.utcnow().isoformat(),
        })

    df=pd.dataframe(transformed_data)
    df.to_csv("transformed_data.csv")

# Default args
default_args = {
    'owner': 'Priyadarshi_Gupta',
    'depends_on_past': False
}

# DAG definition
dag = DAG(
    dag_id="crypto_exchange_pipeline_corrected",
    default_args=default_args,
    start_date=datetime(2021, 1, 1),
    schedule_interval=timedelta(minutes=10),
    catchup=False
)

# Task 1: Fetch data
fetch_data_task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_api_data,
    dag=dag
)

# Task 2: Create GCS bucket
create_bucket_task = GCSCreateBucketOperator(
    task_id='create_bucket',
    bucket_name=GCS_BUCKET,
    storage_class="MULTI_REGIONAL",
    location="US",
    gcp_conn_id="google_cloud_default",
    dag=dag
)

# Task 3: Upload raw data to GCS
upload_raw_to_gcs_task = LocalFilesystemToGCSOperator(
    task_id='upload_raw_data_to_gcs',
    src="crypto_data.json",
    dst=f"{GCS_RAW_DATA_PATH}/crypto_data.json",
    bucket=GCS_BUCKET,
    gcp_conn_id="google_cloud_default",
    dag=dag
)

transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

upload_transformed_data_to_gcs_task = LocalFilesystemToGCSOperator(
    task_id='upload_transformed_data_to_gcs',
    src="tra.json",
    dst=GCS_TRANSFORMED_DATA_PATH+"_{{ts_nodash}}.json,",
    bucket=GCS_BUCKET,
    gcp_conn_id="google_cloud_default",
    dag=dag
)
# Task dependency chain
fetch_data_task >> create_bucket_task >> upload_raw_to_gcs_task
upload_raw_to_gcs_task>> transform_data_task >> upload_transformed_data_to_gcs_task
