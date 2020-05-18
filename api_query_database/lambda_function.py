import json
from custom_utils import mysql_db_utils as db_utils
from custom_utils import rds_config
from custom_utils import s3_utils


def lambda_handler(event, context):
    """
    Get data from database using a query stored in s3, return response.
    """

    # Map API paths to correct SQL query stored in s3
    s3_queries = {
        '/api/parcel-stats-by-city': 'parcel_stats_by_city.sql',
        '/api/parcel-history': 'parcel_history.sql'
    }

    bucket = 'bw-code'
    key = s3_queries[event['path']]

    query_string = s3_utils.download_file_as_string(bucket, key)
    query_params = event['queryStringParameters']

    print('running query: ' + key)

    rows = db_utils.select_query(rds_config.db_params, query_string, query_params)

    return {
        'statusCode': 200,
        'body': json.dumps(rows)
    }
