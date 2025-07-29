import requests
import pandas as pd
import json
from datetime import datetime, date, timedelta
import os
import logging
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

BUCKET_NAME = 's3 bucket name'
TOPIC = 'apple'

logging.basicConfig(level=logging.INFO)

def fetch_news():
    API_KEY = 'api'
    BASE_URL = "https://newsapi.org/v2/everything"
    
    today = date.today()
    start_date = today - timedelta(days=1)

    params = {
        'q': TOPIC,
        'from': start_date.isoformat(),
        'to': today.isoformat(),
        'sortBy': 'popularity',
        'apiKey': API_KEY,
        'language': 'en'
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json().get('articles', [])

def clean_articles(articles):
    rows = []
    for i in articles:
        content = i.get('content') or ''
        if len(content) > 200:
            content = content[:content.rindex('.')] if '.' in content else content[:200]
        rows.append({
            'newsTitle': i.get('title') or '',
            'timestamp': i.get('publishedAt') or '',
            'url_source': i.get('url') or '',
            'content': content,
            'source': i.get('source', {}).get('name') or '',
            'author': i.get('author', '') or '',
            'urlToImage': i.get('urlToImage') or ''
        })
    return pd.DataFrame(rows)

def save_to_parquet(df):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{current_time}_{TOPIC}_news.parquet"
    file_path = f"/tmp/{file_name}"
    df.to_parquet(file_path, index=False)
    return file_path

def upload_to_s3(file_path):
    s3_key = f"news_data/{os.path.basename(file_path)}"
    hook = S3Hook(aws_conn_id="aws_conn")
    hook.load_file(
        filename=file_path,
        key=s3_key,
        bucket_name=BUCKET_NAME,
        replace=True
    )
    return s3_key
