# etl-ticketmaster-aws
 Ticketmaster API - Data Engineer ETL Pipeline
# Ticketmaster ETL Pipeline

This repository showcases an ETL pipeline designed to extract, transform, and load data from the Ticketmaster Discovery API into a structured format suitable for analytics and reporting.

## Architecture Overview

![Ticketmaster ETL Architecture](./TICKETMASTER_ETL.png)

### Components

- **Ticketmaster Discovery API:** The source of event data. This API is polled periodically to retrieve new or updated event information.
  
- **AWS Lambda:** Serves as the orchestrator that pulls data from the API and deposits raw JSON data into the S3 landing bucket.
  
- **Amazon S3 (Landing, Standardized):** S3 is used as the data lake, with a landing zone for raw data and a standardized zone for processed data stored in Parquet format.

- **AWS Glue:** Handles the transformation of raw JSON data into a standardized Parquet format. It also manages the ETL jobs to move data between S3 buckets and loads the final data into the Aurora PostgreSQL database.

- **Amazon Aurora PostgreSQL:** A managed relational database that serves as the data warehouse, enabling efficient querying and analysis.

- **Amazon Athena:** Allows querying of the data stored in S3 using standard SQL. This is particularly useful for exploratory data analysis.

- **Amazon QuickSight:** Provides visualization and reporting capabilities, allowing business users to gain insights from the data.

- **Amazon EventBridge & AWS Step Functions:** These services are used for orchestration and scheduling of the ETL jobs, ensuring data is processed and available in a timely manner.

## ETL Process

1. **Data Extraction:** AWS Lambda is triggered periodically by Amazon EventBridge to pull data from the Ticketmaster Discovery API.
2. **Data Landing:** The raw JSON data is stored in an S3 bucket (Landing Zone).
3. **Data Transformation:** AWS Glue jobs transform the raw data into a standardized Parquet format and store it in another S3 bucket (Standardized Zone).
4. **Data Loading:** Transformed data is loaded into Amazon Aurora PostgreSQL for structured querying and reporting.
5. **Data Consumption:** Using Amazon Athena and QuickSight, the data is made available for querying and visualization.

## Key Features

- **Serverless Architecture:** The pipeline is fully serverless, leveraging AWS managed services to ensure scalability, reliability, and cost efficiency.
  
- **Data Lake and Warehouse Integration:** Combines the flexibility of an S3-based data lake with the structured querying capabilities of a relational database in Aurora.

- **Orchestrated Workflow:** Automated scheduling and error handling through EventBridge and Step Functions.

- **Advanced Reporting:** Integration with Amazon QuickSight allows for rich data visualization and reporting.

## Prerequisites

To deploy this pipeline, you need the following:

- An AWS account with the necessary permissions.
- Access to the Ticketmaster Discovery API.
- AWS CLI or SDK configured.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ticketmaster-etl-pipeline.git

