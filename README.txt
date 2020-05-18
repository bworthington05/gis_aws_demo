The folders in this directory contain code for several AWS Lambda functions that perform
various ETL tasks and expose data through an API.

These are the basic steps of how these functions work:

1. etl_get_arcgis_data retrieves data from an ArcGIS service and saves the data to an s3 bucket.
This Lambda function is scheduled to run at regular intervals with EventBridge.

2. etl_normalize_arcgis_data normalizes the data into a desired format that matches a table in
a MySQL database. It is triggered to run when new data is added to s3 from the first step.

3. etl_save_to_database saves the normalized data from the second step into a MySQL database.
It is triggered to run when new normalized data is added to s3 from the second step.

4. etl_refresh_database_table runs a query to truncate and repopulate a table in the MySQL database
that contains only the most recent records. It is scheduled to run at regular intervals with EventBridge.

5. api_query_database exposes data to a REST API managed by API Gateway.

sql contains SQL scripts for setting up the database and queries run by the Lambda functions above.
These are stored on s3 where they are accessible to Lambda.

custom_utils contains a collection of customized functions for interacting with files on s3
and running SQL queries. These functions are used by multiple Lambda functions and copied when
the functions are created on AWS.

Each Lambda folder contains a shell script called create_function.sh. This script packages the code
and all dependenices into a zip file, which is uploaded to AWS. The script requires that the
AWS CLI tool (version2) is installed locally. It also assumes that the relevant IAM roles and policies have
been created first. There are a few additional steps not covered by the shell script that must be completed,
such as setting up API Gateway, creating VPC endpoints, etc.

Below are examples of GET requests to the two endpoints that are managed by API Gateway and processed by Lambda:

1. Get computed statistics about parcels grouped by city.

curl --location --request GET 'https://qgyjri8fab.execute-api.us-east-1.amazonaws.com/prod/api/parcel-stats-by-city?dataset=cupertino' \
--header 'x-api-key: ****'

Response:

[
    {
        "city": "CUPERTINO",
        "count_of_parcels": "15474",
        "average_parcel_area": "16962.9720",
        "minimum_parcel_area": "1.9580",
        "maximum_parcel_area": "9408525.7539"
    },
    {
        "city": "LOS ALTOS",
        "count_of_parcels": "850",
        "average_parcel_area": "15124.7128",
        "minimum_parcel_area": "285.9258",
        "maximum_parcel_area": "477519.4131"
    },
    {
        "city": "SAN JOSE",
        "count_of_parcels": "2732",
        "average_parcel_area": "9833.1187",
        "minimum_parcel_area": "262.5117",
        "maximum_parcel_area": "757960.5771"
    },
    ....
]

2. Get the history for a given parcel, based on however much data has been collected over time from the ArcGIS service.

curl --location --request GET 'https://qgyjri8fab.execute-api.us-east-1.amazonaws.com/prod/api/parcel-history?dataset=cupertino&apn=359%2031%20031' \
--header 'x-api-key: ****'

[
    {
        "id": 83031,
        "dataset": "cupertino",
        "as_of": "2020-05-18 03:19:18",
        "apn": "359 31 031",
        "objectid": "43946",
        "city": "CUPERTINO",
        "x_coordinate": "6115377.7698",
        "y_coordinate": "6058.2013",
        "area": "6058.1865",
        "length": "328.6443"
    },
    {
        "id": 60550,
        "dataset": "cupertino",
        "as_of": "2020-05-17 21:19:18",
        "apn": "359 31 031",
        "objectid": "43946",
        "city": "CUPERTINO",
        "x_coordinate": "6115377.7698",
        "y_coordinate": "6058.2013",
        "area": "6058.1865",
        "length": "328.6443"
    },
    {
        "id": 38069,
        "dataset": "cupertino",
        "as_of": "2020-05-17 15:19:19",
        "apn": "359 31 031",
        "objectid": "43946",
        "city": "CUPERTINO",
        "x_coordinate": "6115377.7698",
        "y_coordinate": "6058.2013",
        "area": "6058.1865",
        "length": "328.6443"
    },
    {
        "id": 15588,
        "dataset": "cupertino",
        "as_of": "2020-05-17 09:19:18",
        "apn": "359 31 031",
        "objectid": "43946",
        "city": "CUPERTINO",
        "x_coordinate": "6115377.7698",
        "y_coordinate": "6058.2013",
        "area": "6058.1865",
        "length": "328.6443"
    }
]
