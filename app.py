import os
import sys
import logging
import logging.handlers
import time
import requests
import boto3
from boto3.dynamodb.conditions import Key

# This code uses the following environment variables passed from docker's env file
# APP_NAME
# POST URL
# SLEEP_TIME

## AWS crdentials for accessing AWS Dynamo DB
# AWS_KEY
# AWS_SECRET
# AWS_REGION

## AWS Dynamo DB table, query key and query value
# DYNAMO_TABLE
# DYNAMO_QUERY_KEY
# DYNAMO_QUERY_VALUE

sleep_time = float(os.environ['SLEEP_TIME'])*60
post_url = os.environ['POST_URL']
db = boto3.resource( 'dynamodb', 
        region_name=os.environ['AWS_REGION'], 
        aws_access_key_id=os.environ['AWS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET'])
table = db.Table(os.environ['DYNAMO_TABLE'])
query_key = os.environ['DYNAMO_QUERY_KEY']
query_value = os.environ['DYNAMO_QUERY_VALUE']

#
# This functions creates a logger for this application
# we use the stdout logger handle and print all logs to stdout
# The caller can redirect this to any log file
#
def configure_logging():
    _logger = logging.getLogger('APP')
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    ch.setFormatter(formatter)
    _logger.addHandler(ch)
    return _logger

# 
# This function performs the actual dynamo query
# The inputs are:
#   tbl - A handle to the Dynamo DB Table, the table name comes from the environment variable DYNAMO_TABLE
#   key - This is the key we  search for
#   value - The value we are searching for
#
# Returns the items from the response or An empty array if no matching values are found
def perform_dynamo_query(tbl, key, value):
    response = tbl.query(KeyConditionExpression=Key(key).eq(value))
    return response['Items']

#
# This function performs the entire service of performing the Dynamo DB query and 
# posting the results to the provided POST URL
#
def start():
    try:
        db_results = perform_dynamo_query(table, query_key, query_value)
        if len(db_results) == 0:
            logger.error(F"Failed: No matching Dynamo results:")
        else:
           res = requests.post(post_url, data=db_results[0])
           if res.status_code == 200:
               logger.debug(F"Success: Posted HTTP Data to {post_url}: {res.status_code}")
           else:
               logger.debug(F"Failure: posting HTTP Data: {res.status_code}")
    except Exception as e:
        logger.error(F"Failure: Exception: {e}")


# Currently, the main loop uses a simple sleep between executions. The sleep time is provided in minutes
# but the call here uses it in seconds
if __name__ == "__main__":
    logger = configure_logging()
    while True:
        start()
        time.sleep(sleep_time)
