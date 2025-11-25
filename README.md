
This project is a complete end-to-end data pipeline built using Apache Airflow, leveraging the CoinGecko API to fetch live cryptocurrency market data, transform it into a structured format, and store both raw and processed data in Google Cloud Storage (GCS).
The pipeline is automated, scalable, and designed to run every 10 minutes.

🚀 Project Purpose

Cryptocurrency data changes rapidly, and having a reliable pipeline to automatically collect, process, and store this data is very valuable for analysis, reporting, or building dashboards.
This pipeline solves that by:

✔ Fetching the latest crypto data
✔ Transforming it into structured format (CSV)
✔ Uploading both raw and processed files to GCS
✔ Organizing data by timestamp for future use

🛠️ Tech Stack
Component	Technology
Orchestration	Apache Airflow
Data Source	CoinGecko API
Cloud Storage	Google Cloud Storage (GCS)
Programming Language	Python
Libraries Used	pandas, requests, datetime, json
Airflow Providers	apache-airflow-providers-google
📂 Project Folder Structure
crypto-exchange-pipeline/
│
├── dags/
│   └── crypto_exchange_pipeline_corrected.py
│
├── crypto_data.json
├── transformed_data.csv
├── requirements.txt
└── README.md

🔄 Pipeline Workflow
1️⃣ Fetch Data from CoinGecko API  
2️⃣ Save data locally as crypto_data.json  
3️⃣ Create a GCS bucket (if not exists)  
4️⃣ Upload raw JSON file to GCS  
5️⃣ Transform JSON into structured CSV  
6️⃣ Upload transformed CSV to GCS with timestamp

📊 Fields Extracted from API

Each cryptocurrency record includes:

ID
Name
Symbol
Current Price
Market Cap
Total Volume
Last Updated Time

Pipeline timestamp (UTC format)

⚙️ Google Cloud Configuration
GCP_PROJECT = "learn-airflow-428415"
GCS_BUCKET = "crypto-exchange-pipeline-priyadarshigupta"
GCS_RAW_DATA_PATH = "raw_data/crypto_raw_data"
GCS_TRANSFORMED_DATA_PATH = "transformed_data/crypto_raw_data"

⏲ Schedule

The DAG is configured to run every 10 minutes, ensuring near real-time data availability.

 DAG Visualization
fetch_data_task
        ↓
create_bucket_task
        ↓
upload_raw_data_to_gcs
        ↓
transform_data_task
        ↓
upload_transformed_data_to_gcs

▶️ How to Run the Project
1️⃣ Install Required Libraries
pip install apache-airflow apache-airflow-providers-google pandas requests

2️⃣ Place your DAG file in Airflow DAGs folder
/opt/airflow/dags/crypto_exchange_pipeline_corrected.py

3️⃣ Initialize Airflow and Start Services
airflow db init
airflow webserver --port 8080
airflow scheduler

4️⃣ Open Airflow UI and Activate the DAG

Open: http://localhost:8080

Search for: crypto_exchange_pipeline_corrected

Turn toggle ON

📤 Output Stored in Google Cloud

Raw Data:

gs://crypto-exchange-pipeline-priyadarshigupta/raw_data/crypto_raw_data/crypto_data.json


Transformed Data:

gs://crypto-exchange-pipeline-priyadarshigupta/transformed_data/crypto_raw_data/transformed_data_202502051005.csv

🧾 Common Issues & Fixes
Issue	Reason	Fix
data=json.load(data,f)	Wrong syntax	Use data = json.load(f)
pd.dataframe error	Wrong function name	Use pd.DataFrame()
tra.json file not found	Incorrect filename	Replace with "transformed_data.csv"
Missing API keys	CoinGecko doesn’t need keys	Works without credentials
Undefined fields in API	Fields not available	Use item.get('field_name')
🌟 Future Improvements

🔹 Load transformed data into BigQuery
🔹 Add Spark for heavy data processing
🔹 Build Tableau / Power BI dashboard
🔹 Add Slack / Email alerts on DAG failure

🤝 Want to Contribute?

Feel free to fork this repository, make improvements, and raise pull requests.
All meaningful contributions are welcome!

📝 License

This project is licensed under the MIT License.

🙌 Author

Priyadarshi Gupta
Data Engineering Enthusiast | Cloud & ETL Learner
