from custom_utils import mysql_db_utils as db_utils
from custom_utils import rds_config
from custom_utils import s3_utils
from urllib.parse import unquote_plus


def lambda_handler(event, context):
    """
    Refresh data in a table using a query stored in s3.
    """

    bucket = event['s3']['bucket']['name']
    key = unquote_plus(event['s3']['object']['key'])
    table = event['database']['table']

    query_string = s3_utils.download_file_as_string(bucket, key)

    print('refreshing table: ' + table)

    rows = db_utils.select_query(rds_config.db_params, query_string)

    if len(rows) == 0:
        print('query returned 0 rows, taking no action')
    else:
        # Get list of column names from the first row in the results
        column_names = [k for k in rows[0].keys()]
        db_utils.truncate_table(rds_config.db_params, table)
        db_utils.insert_rows(rds_config.db_params, table, column_names, rows)
        print('table refresh complete')
