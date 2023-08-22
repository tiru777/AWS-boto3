import boto3
import json
from pprint import pprint

iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')

role_policy = {

    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }

    ]

}


def create_iam_lambda_role():
    response = iam_client.create_role(
        RoleName='PyLambdaBasicExecution',
        AssumeRolePolicyDocument=json.dumps(role_policy)

    )

    return response


def create_lambda_function():
    """
    # zipped code of lambda
    def lambda_handler(event, context):
    return {
    'statusCode':200,
    'body':json.dumps("Hello From Python & Boto3")
    }
    """
    with open('lambda.zip', 'rb') as f:
        # we are uploading zip file to lambda using hellowWorldLambda function
        zipped_code = f.read()

    role = iam_client.get_role(RoleName='PyLambdaBasicExecution')
    pprint(role)
    response = lambda_client.create_function(
        FunctionName='helloWorldLambda',
        Runtime='python3.9',
        Role=role['Role']['Arn'],
        Handler='lambda_function.lambda_handler',
        Code=dict(ZipFile=zipped_code),
        Timeout=300,

    )

    return response


def invoke_function():
    test_event = dict()

    response = lambda_client.invoke(
        FunctionName='helloWorldLambda',
        Payload=json.dumps(test_event)
    )

    print(response['Payload'])
    print(response['Payload'].read().decode('utf-8')) # give response as result in json format


def describe_lambda_func():

    response = lambda_client.get_function(
        FunctionName='helloWorldLambda'
    )

    return response


def delete_lambda_func():

    response = lambda_client.delete_function(
        FunctionName='helloWorldLambda'
    )

    return response


# print(create_iam_lambda_role())
# print(create_lambda_function())
# invoke_function()
# print(describe_lambda_func())
print(delete_lambda_func())

