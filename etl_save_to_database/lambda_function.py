import json
from custom_utils import mysql_db_utils as db_utils
from custom_utils import rds_config
from custom_utils import s3_utils
from urllib.parse import unquote_plus


def lambda_handler(event, context):
    """
    Save data from s3 to database.
    """

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        str_value = s3_utils.download_file_as_string(bucket, key)
        data = json.loads(str_value)

        table = data['meta']['table']
        column_names = data['meta']['column_names']
        rows = data['rows']

        db_utils.insert_rows(rds_config.db_params, table, column_names, rows)

    print('s3 data saving complete')
