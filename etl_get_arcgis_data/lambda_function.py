import random
import requests
import time
from datetime import datetime
from custom_utils import s3_utils


def wait_with_exponential_backoff(attempt_number):
    """
    Wait for an exponentially increasing number of seconds based on how many
    attempts have been made.
    Requires the following arguments:
        1 - the attempt number
    """

    wait_time = (2 ** attempt_number) + (random.randint(0, 1000) / 1000.0)
    print('\nwaiting ' + str(wait_time) + ' seconds...\n')
    time.sleep(wait_time)


def try_request(url, query_params):
    """
    Try to make a GET request and return the JSON response if successful.
    Requires the following arguments:
        1 - the url
        2 - dictionary with query params
    """
    
    max_attempts = 5
    
    for n in range(0, max_attempts):
        try:
            response = requests.request('GET', url, params=query_params)
            print('requested: ' + response.request.url)

            # First check if status code indicates an error
            response.raise_for_status()

            # Also check for errors in the response body because the service
            # may return a 200 code but include error messages in the response
            response_json = response.json()

            if 'error' in [k.lower() for k in response_json.keys()]:
                raise ValueError(response_json)

            return response_json
        
        except Exception as e:
            if n < max_attempts:
                print(e)
                wait_with_exponential_backoff(n)
            else:
                raise 


def get_total_count(url):
    """
    Get total count of features from an ArcGIS service.
    Requires the following arguments:
        1 - the url
    """
    query_params = {
        'where': '1=1',
        'returnCountOnly': True,
        'f': 'json'
    }
    
    response_json = try_request(url, query_params)
    return response_json['count']


def get_all_features(url):
    """
    Get all features from an ArcGIS service.
    Requires the following arguments:
        1 - the url
    """

    results = []

    query_params = {
        'where': '1=1',
        'outFields': '*',
        'returnGeometry': False,
        'resultRecordCount': 1000,
        'f': 'json'
    }
    
    result_offset = 0
    
    exceeded_transfer_limit = True

    while exceeded_transfer_limit:
        
        query_params['resultOffset'] = result_offset
        
        response_json = try_request(url, query_params)
        
        # Prepare for requesting next batch of results
        exceeded_transfer_limit = response_json.get('exceededTransferLimit', False)
        result_offset += 1000
        
        results.extend(response_json['features'])

    return results



def lambda_handler(event, context):
    """
    Retrieve data from an ArcGIS service and save on s3.
    """

    url = event['gis']['url']
    dataset = event['gis']['dataset']
    bucket = event['s3']['bucket']['name']
    
    total_count = get_total_count(url)
    
    results = get_all_features(url)
    
    if total_count != len(results):
        msg = 'expected %s features but got %s' % (total_count, len(results))
        raise ValueError(msg)
    
    now = datetime.utcnow()

    data = {
        'meta': {
            'dataset': dataset,
            'datetime': now.strftime('%Y-%m-%d %H:%M:%S')
        },
        'results': results
    }

    timestamp = str(int(now.timestamp()))
    file_name = dataset + '_' + timestamp + '.json'
    s3_utils.upload_json_as_file(data, bucket, file_name)
