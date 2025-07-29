USE ROLE ACCOUNTADMIN;

CREATE DATABASE news_database;


USE news_database;

CREATE OR REPLACE FILE FORMAT parquet_format TYPE=parquet;

-- create storage integration
CREATE OR REPLACE STORAGE INTEGRATION news_data_s3_integration
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 'S3'
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::880265509658:role/snowflakerole'
STORAGE_ALLOWED_LOCATIONS = ('s3://my-news-bucket-varshith/news_data/');


DESC INTEGRATION news_data_s3_integration;

CREATE OR REPLACE STAGE s3_raw_data_stage
URL = 's3://my-news-bucket-varshith/news_data/'
STORAGE_INTEGRATION = news_data_s3_integration
FILE_FORMAT = (TYPE = 'PARQUET');

-- check stage
LIST @s3_raw_data_stage;


SELECT * FROM AUTHOR_ACTIVITY;
