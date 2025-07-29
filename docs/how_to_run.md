# 🛠️ How to Run This Project

This guide outlines how to run the **Event-Driven News Ingestion Pipeline** using the provided Airflow DAG, Python script, and Snowflake SQL setup.

---

## ✅ Steps to Run

### 1️⃣ Set Up Your Cloud Services

Make sure you have:

- A valid **AWS S3 bucket** for storing Parquet files
- A **Snowflake account** with `ACCOUNTADMIN` or equivalent privileges
- A **NewsAPI key** (you can get one from [https://newsapi.org](https://newsapi.org))

---

### 2️⃣ Use the Provided Scripts

This project includes everything you need:

- Python ETL logic:  
  `scripts/fetch_news_etl_job.py`

- Airflow DAG:  
  `dags/news_pipeline_airflow_dag.py`

- Snowflake setup :  
  `snowflake/snowflake_script.sql`

All logic is modular and tied together through Airflow.

---

### 3️⃣ Replace Hidden Values

Before running the project, replace the following placeholders with your own values:

- **S3 Bucket Name**  
  `s3-bucket-name` → your actual S3 bucket

- **IAM Role ARN**  
  Replace `STORAGE_AWS_ROLE_ARN` in `snowflake_script.sql` with your actual AWS IAM role that has S3 access

- **Airflow Connection IDs in astronomer**  
  Use your own or set up:
  - `aws_conn` (Amazon Web Services connection)
  - `snowflake_conn` (Snowflake connection)

- **NewsAPI Key**  
  Add your News API key to the ETL script or via environment variables.

---

### 4️⃣ Run the Project with Astronomer Recommended

If you're using terminal:

```

astro login   #for connecting to astronomer cloud

astro dev init   # for initializing the setup for airflow

astro deploy  # for deploying the script to astronomer airflow

```


