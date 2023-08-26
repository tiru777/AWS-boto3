import boto3


cf_client = boto3.client('cloudformation')
# cf = boto3.resource('cloudformation')


def create_stack():
    """
    it will create stack with dynamo table
    """
    with open('Dynamodb.yml', 'r') as f:
        dy_template = f.read()

    params = [
        {
            'ParameterKey': 'HashKeyElementName',
            'ParameterValue':'EmployeeId'
        }

    ]

    response = cf_client.create_stack(
        StackName='dynamobotostack',
        TemplateBody=dy_template,
        Parameters=params

    )
    return response


def describe_stack(stack_name):
    response = cf_client.describe_stacks(
        StackName=stack_name
    )

    return response


def get_template(stack_name):
    response = cf_client.get_template(
        StackName=stack_name
    )

    # pprint(response)
    return response['TemplateBody']


def delete_stack(stack_name):
    response = cf_client.delete_stack(
        StackName=stack_name
    )

    # pprint(response)
    return response


# print(create_stack())
# print(describe_stack('dynamobotostack'))
# print(get_template('dynamobotostack'))
# print(delete_stack('dynamobotostack'))
print(delete_stack('dynamodbstack'))

