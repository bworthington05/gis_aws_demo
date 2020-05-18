# This script assumes the relevant IAM role exists

echo creating AWS Lambda function...

rm function.zip

rm -r package

python3.8 -m pip install --target ./package mysql-connector-python boto3

cd package

zip -r9 ${OLDPWD}/function.zip .

cd $OLDPWD

zip -g function.zip lambda_function.py

zip -g function.zip ../custom_utils/__init__.py
zip -g function.zip ../custom_utils/s3_utils.py
zip -g function.zip ../custom_utils/mysql_db_utils.py
zip -g function.zip ../custom_utils/rds_config.py

aws lambda create-function \
--function-name etl-save-to-database \
--runtime python3.8 \
--role arn:aws:iam::778775561213:role/lambda-vpc-role \
--handler lambda_function.lambda_handler \
--timeout 600 \
--memory-size 256 \
--zip-file fileb://function.zip \

# Example of updating existing function
# aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip

# Also need to create a trigger event so this function runs when a new file is added to s3

# Configure VPC settings

# Because this Lambda is operating in a VPC, it can't connect to s3 by default, must configure a VPC endpoint for it:
# https://aws.amazon.com/blogs/aws/new-vpc-endpoint-for-amazon-s3/
