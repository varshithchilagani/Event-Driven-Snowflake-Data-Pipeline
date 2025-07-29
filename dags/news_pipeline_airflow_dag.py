from airflow import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
from scripts import fetch_news_etl_job
import pandas as pd

default_args = {
    'owner': 'varshith',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='news_api_etl_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 7, 24),
    schedule="@daily",
    catchup=False
) as dag:

    @task()
    def fetch_news_task():
        return fetch_news_etl_job.fetch_news()

    @task()
    def clean_articles_task(articles):
        df = fetch_news_etl_job.clean_articles(articles)
        return df.to_json()

    @task()
    def save_and_upload_task(df_json):
        df = pd.read_json(df_json)
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_apple_news.parquet"
        local_path = f"/tmp/{filename}"
        df.to_parquet(local_path)

        # ✅ Upload to S3 using S3Hook
        hook = S3Hook(aws_conn_id="aws_conn")
        hook.load_file(
            filename=local_path,
            key=f"news_data/{filename}",
            bucket_name="my-news-bucket-varshith",
            replace=True
        )
        return f"s3://my-news-bucket-varshith/news_data/{filename}"

    # DAG flow
    articles = fetch_news_task()
    cleaned_df = clean_articles_task(articles)
    parquet_path = save_and_upload_task(cleaned_df)

    # Snowflake Tasks
    create_table = SQLExecuteQueryOperator(
        task_id = 'create_snowflake_table',
        sql = """CREATE TABLE IF NOT EXISTS news_database.PUBLIC.news_data USING TEMPLATE (
                SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
                FROM TABLE(INFER_SCHEMA (
                    LOCATION => '@news_database.PUBLIC.s3_raw_data_stage',
                    FILE_FORMAT => 'parquet_format'
                ))
            )""",
        conn_id="snowflake_conn"
    )

    copy_into_table = SQLExecuteQueryOperator(
        task_id="snowflake_copy_from_stage",
        sql="""COPY INTO news_database.PUBLIC.news_data
            FROM @news_database.PUBLIC.s3_raw_data_stage
            MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE 
            FILE_FORMAT = (FORMAT_NAME = 'parquet_format') 
            """,
        conn_id="snowflake_conn"
    )

    create_summary = SQLExecuteQueryOperator(
         task_id="create_or_replace_news_summary_table",
        sql="""
        CREATE OR REPLACE TABLE news_database.PUBLIC.summary_news AS
        SELECT
            "source" AS news_source,
            COUNT(*) AS article_count,
            MAX("timestamp") AS latest_article_date,
            MIN("timestamp") AS earliest_article_date
        FROM news_database.PUBLIC.news_data as tb
        GROUP BY "source"
        ORDER BY article_count DESC;
        """,
        conn_id="snowflake_conn"
    )

    create_author_activity = SQLExecuteQueryOperator(
        task_id="create_or_replace_author_activity_table",
    sql="""
        CREATE OR REPLACE TABLE news_database.PUBLIC.author_activity AS
        SELECT
            "author",
            COUNT(*) AS article_count,
            MAX("timestamp") AS latest_article_date,
            COUNT(DISTINCT "source") AS distinct_sources
        FROM news_database.PUBLIC.news_data as tb
        WHERE "author" IS NOT NULL
        GROUP BY "author"
        ORDER BY article_count DESC;
    """,
    conn_id="snowflake_conn"
    )

# Task dependencies
parquet_path >> create_table >> copy_into_table >> [create_summary, create_author_activity]
