import json
from custom_utils import s3_utils
from urllib.parse import unquote_plus


def lambda_handler(event, context):
    """
    Normalize and save data on s3.
    """

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        str_value = s3_utils.download_file_as_string(bucket, key)
        data = json.loads(str_value)

        normalized_data = {
            'meta': {
                'table': 'parcels',
                'column_names': [
                    'dataset',
                    'as_of',
                    'apn',
                    'objectid',
                    'city',
                    'x_coordinate',
                    'y_coordinate',
                    'area',
                    'length'
                ]
            }
        }

        rows = []

        dataset = data['meta']['dataset']
        as_of = data['meta']['datetime']

        for r in data['results']:

            attr = r['attributes']

            temp_dict = {
                'dataset': dataset,
                'as_of': as_of,
                'apn': attr.get('APN_SPACE'),
                'objectid': attr.get('OBJECTID'),
                'city': attr.get('CITY'),
                'x_coordinate': attr.get('X'),
                'y_coordinate': attr.get('Y'),
                'area': attr.get('Shape.STArea()'),
                'length': attr.get('Shape.STLength()')
            }

            rows.append(temp_dict)

        normalized_data['rows'] = rows
        
        bucket = 'gis-data-normalized'
        file_name = 'normalized_' + key
        s3_utils.upload_json_as_file(normalized_data, bucket, file_name)
