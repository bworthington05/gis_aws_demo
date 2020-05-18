# This script assumes the relevant IAM role exists

echo creating AWS Lambda function...

rm function.zip

rm -r package

python3.8 -m pip install --target ./package requests boto3

cd package

zip -r9 ${OLDPWD}/function.zip .

cd $OLDPWD

zip -g function.zip lambda_function.py

zip -g function.zip ../custom_utils/__init__.py
zip -g function.zip ../custom_utils/s3_utils.py

aws lambda create-function \
--function-name etl-get-arcgis-data \
--runtime python3.8 \
--role arn:aws:iam::778775561213:role/lambda-ex \
--handler lambda_function.lambda_handler \
--timeout 600 \
--memory-size 256 \
--zip-file fileb://function.zip

# Example of updating existing function
# aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip

# Also need to create an EventBridge schedule to trigger this function to run every X hours
# Use test_event.json for the format of the event
