# Event-Driven News Data Ingestion and Structuring in Snowflake using Snowpipe, S3, and Airflow

This project builds an automated, event-driven data pipeline that fetches news articles from a public API, stores the data in AWS S3 as Parquet files, and ingests it into Snowflake using Snowpipe. The entire pipeline is orchestrated and scheduled using Apache Airflow. The final data is structured into meaningful summary tables inside Snowflake.

---

## 🛠️ Tech Stack

- **Python** – for API integration and data cleaning
- **AWS S3** – for raw Parquet file storage
- **Snowflake** – for data staging, storage, and transformation
- **Snowpipe** – for continuous, automated data ingestion
- **Apache Airflow** – for pipeline scheduling and orchestration
- **NewsAPI** – data source (news articles)

---

## 📊 Architecture

![Architecture Diagram](./architecture_diagram.png)

---

## 📂 Folder Structure

```
event-driven-snowflake-data-pipeline/
│
├── dags/
│ └── news_api_airflow_job.py # Airflow DAG file
│
├── scripts/
│ └── fetch_news.py # API fetch and upload to S3
│
├── snowflake/
│ └── snowflake_commands.sql # DDL & stage setup
│
├── docs/
│ └── architecture_diagram.png # Visual overview (to be added)
│
├── README.md # Project documentation
└── requirements.txt # Python dependencies
```

---

## ⚙️ Pipeline Overview

1. Airflow triggers the DAG daily
2. `fetch_news.py`:
   - Pulls news from the NewsAPI
   - Cleans and formats the data
   - Saves as a `.parquet` file
   - Uploads to AWS S3
3. Snowpipe listens to S3 and ingests the Parquet file into Snowflake
4. Airflow triggers SnowflakeOperator SQL tasks:
   - Creates staging and final tables
   - Populates summary tables (`summary_news`, `author_activity`)

---

## 📝 SQL Logic (in Snowflake)

- Create stage using S3
- Auto-create table using `INFER_SCHEMA`
- Load data using `COPY INTO`
- Create summary tables:
  - `summary_news`: article count per news source
  - `author_activity`: article count per author




