import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, when, to_timestamp
from pyspark.sql.types import IntegerType
from utils.pull_api_utils import add_timestamp_to_filename
from utils import variables as V

## @params: [JOB_NAME], Get the S3_INPUT_PATH from the arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH'])
print(args)


# Initialize Spark session
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


# Load the data
df = spark.read.format('parquet').load(args['S3_INPUT_PATH']).cache()

# Data Cleaning and Transformation
df.printSchema()

# Remove empty event_date, min_price, max_price
df_cleaned = df.filter(col("event_date",).isNotNull())
df_cleaned = df_cleaned.filter(col("min_price").isNotNull())
df_cleaned = df_cleaned.filter(col("max_price").isNotNull())


# Define the date format
date_format = "yyyy-MM-dd'T'HH:mm:ss'Z'"

# Standardize date columns from string to timestamp using the specified format
df_cleaned = df_cleaned.withColumn("event_date", to_timestamp(col("event_date"), date_format))
df_cleaned = df_cleaned.withColumn("event_sales_start_date", to_timestamp(col("event_sales_start_date"), date_format))
df_cleaned = df_cleaned.withColumn("event_sales_end_date", to_timestamp(col("event_sales_end_date"), date_format))

# Cast price fields to float
df_cleaned = df_cleaned.withColumn("min_price", col("min_price").cast("float"))
df_cleaned = df_cleaned.withColumn("max_price", col("max_price").cast("float"))


# Replace null values in 'promoter_name' with 'Unknown'
df_cleaned = df_cleaned.withColumn("promoter_name", when(col("promoter_name").isNull(), "Unknown").otherwise(col("promoter_name")))


# Add a new column for the duration of the event sales period
df_cleaned = df_cleaned.withColumn("sales_duration_days", 
                   ((col("event_sales_end_date").cast("long") - col("event_sales_start_date").cast("long")) / (60 * 60 * 24)).cast(IntegerType()))

# Add a new column for average price
df_cleaned = df_cleaned.withColumn("average_price", (col("min_price") + col("max_price")) / 2)

# df_cleaned.show()

#TODO: Glue aggregate: thành phố có bn concert, events 

# Write the transformed data to gold Parquet
object_key = add_timestamp_to_filename(V.GOLDEN_ZONE)
bucket_name = V.DATA_LANDING_BUCKET_NAME
s3_saving_path = f's3://{bucket_name}/gold/{object_key}'

# Write to S3 gold bucket
df_cleaned.write.mode('overwrite').parquet(s3_saving_path)
print(f'Successfully uploaded the Parquet to {s3_saving_path}')


job.commit()