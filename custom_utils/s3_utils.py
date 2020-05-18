import boto3
import io
import json


s3_client = boto3.client('s3')


def upload_json_as_file(data, bucket, key):
    """
    This function converts a list or dictionary to a JSON string
    and uploads it to an s3 bucket as a .json file.
    Requires the following arguments:
        1 - the data, a list or dictionary
        2 - the bucket name
        3 - the s3 object key (or file name)
    """

    print('uploading to s3 bucket: ' + bucket)
    fileobj = io.BytesIO(json.dumps(data).encode('utf-8'))
    s3_client.upload_fileobj(fileobj, bucket, key)
    print('upload complete')


def download_file_as_string(bucket, key):
    """
    This function downloads a file from s3 and returns it as a string.
    Requires the following arguments:
        1 - the bucket name
        2 - the s3 object key (or file name)
    """

    print('reading s3 data object: ' + key)
    bytes_buffer = io.BytesIO()
    s3_client.download_fileobj(bucket, key, bytes_buffer)
    byte_value = bytes_buffer.getvalue()
    return byte_value.decode('utf-8')
