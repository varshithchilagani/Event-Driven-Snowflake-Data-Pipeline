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

> (Diagram goes here – will be added under `/docs/architecture_diagram.png`)

