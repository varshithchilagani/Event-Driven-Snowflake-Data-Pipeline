USE ROLE ACCOUNTADMIN;

CREATE DATABASE news_database;


USE news_database;

CREATE OR REPLACE FILE FORMAT parquet_format TYPE=parquet;

-- create storage integration
CREATE OR REPLACE STORAGE INTEGRATION news_data_s3_integration
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 'S3'
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'enter arn'
STORAGE_ALLOWED_LOCATIONS = ('s3://s3-bucket-name/folder-name/');


DESC INTEGRATION news_data_s3_integration;

CREATE OR REPLACE STAGE s3_raw_data_stage
URL = 's3://s3-bucket-name/folder-name/'
STORAGE_INTEGRATION = news_data_s3_integration
FILE_FORMAT = (TYPE = 'PARQUET');

-- check stage
LIST @s3_raw_data_stage;


SELECT * FROM AUTHOR_ACTIVITY;
