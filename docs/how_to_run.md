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

- **Python ETL logic**  
  `scripts/fetch_news_etl_job.py`

- **Airflow DAG**  
  `dags/news_pipeline_airflow_dag.py`

- **Snowflake setup**  
  `snowflake/snowflake_script.sql`

All logic is modular and tied together through Airflow tasks.

---

### 3️⃣ Replace Hidden Values

Before running the project, replace the following placeholders with your own values:

- **S3 Bucket Name**  
  Replace `s3-bucket-name` with your actual S3 bucket name.

- **IAM Role ARN**  
  Update `STORAGE_AWS_ROLE_ARN` in `snowflake_script.sql` with your AWS IAM role that has access to S3.

- **Airflow Connection IDs (in Astronomer)**  
  Configure these inside the Astronomer UI:
  - `aws_conn` → Amazon Web Services connection (with AWS access keys)
  - `snowflake_conn` → Snowflake connection (with account, user, warehouse, role, etc.)

- **NewsAPI Key**  
  Add your News API key in the ETL script or via Airflow Variables.

---

### 4️⃣ Run the Project with Astronomer Cloud 

In your terminal:

```bash
astro login          # Connect to your Astronomer Cloud account
astro dev init       # Initialize the local project structure
astro deploy         # Deploy the DAG and scripts to Astronomer Airflow

```

---

## Output

Once the pipeline runs successfully, the following results will be produced:

✅ A Parquet file will be generated from the API response and uploaded to your AWS S3 bucket

✅ Snowpipe will detect the new file and ingest it into the news_data table in Snowflake

✅ Two summary tables will be automatically created and populated (summary_news and author_activity)
