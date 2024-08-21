import boto3
import logging
import traceback
import os
from utils.pull_api_utils import fetch_ticketmaster_events, add_timestamp_to_filename
from utils import variables as V

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    try:
        logger.info(f"EVENT: {event}")
        logger.info(f"CONTEXT: {context}")


        # Define your API key and endpoint
        api_key = os.environ['TICKETMASTER_API_KEY']
        endpoint = 'https://app.ticketmaster.com/discovery/v2/events.json'
        size = 200
        countryCode = 'US'
        genreID = 'KnvZfZ7vAv1'
        sort = 'date,asc'
        startDateTime = '2024-08-31T01:57:00Z'
        subGenreId = 'KZazBEonSMnZfZ7vaa1'
        locale = '*'


        # Fetch the events and write to JSON
        json_object = fetch_ticketmaster_events(api_key, locale, startDateTime, size, countryCode, genreID, subGenreId, sort, endpoint)
        
        # Initialize the S3 client
        s3_client = boto3.client('s3')
        
        # Specify S3 Bucket and Object
        bucket_name = V.DATA_LANDING_BUCKET_NAME
        object_key = add_timestamp_to_filename(V.RAW_ZONE)
        s3_saving_path = f's3://{bucket_name}/bronze/{object_key}'
    
        # Upload the CSV to S3

        s3_client.put_object(
            Body=json_object, 
            Bucket=bucket_name,
            Key=object_key
        )

        print(f'Successfully uploaded the CSV to {s3_saving_path}')


        return {"status": "SUCCESS"}
    except Exception as ex:
        logger.error(f'FATAL ERROR: {ex} %s')
        logger.error('TRACEBACK:')
        logger.error(traceback.format_exc())

        return {"status": "FAIL", "error": f"{ex}"}