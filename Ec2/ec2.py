import boto3
from pprint import pprint

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

def describe():
    response = ec2_client.describe_instances()

    return response


def create_key_pair():

    resp = ec2_client.create_key_pair(
        KeyName='tiru',
        KeyType='rsa'
    )

    # pprint(resp['KeyMaterial'])
    # store the pem file
    with open('tiru.pem', 'w') as fp:
        fp.write(resp['KeyMaterial'])


def delete_key_pair(key_name):
    resp = ec2_client.delete_key_pair(KeyName=key_name)
    return resp


def create_instance():
    response = ec2_resource.create_instances(
        ImageId='ami-0a709bebf4fa9246f',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='Linux-EC2-Sydney',
        SecurityGroups=[
            'database_Security'
        ]
    )

    return response


def list_instances():

    reservations = ec2_client.describe_instances().get('Reservations')
    """if we know instance id we can use direct
    # reservations = ec2_client.describe_instances().(InstanceIds=[instance_id]).get('Reservations')"""

    for reservation in reservations:
        # pprint(reservation['Instances'])
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            public_ip = instance['PublicIpAddress']
            private_ip = instance['PrivateIpAddress']

            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")


def stop_instance(instance_id):
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    return response


def terminate_instance(instance_id):
    return ec2_client.terminate_instances(InstanceIds=[instance_id])


def create_security_group():
    response = ec2_client.create_security_group(
        Description="This is desc",
        GroupName="pygroup",
        VpcId='vpc-014f67f5e659aed76 '
    )

    return response


def security_group_describe():
    return ec2_client.describe_security_groups() # all security groups description


def security_group_delete(sg_id):
    response = ec2_client.delete_security_group(
        GroupId=sg_id
    )
    return response


def security_group_ingress(sg_id):
    response = ec2_client.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'My description'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'My description'}]
            }
        ]
    )

    return response


# print(describe())
# create_key_pair()
# print(delete_key_pair('tiru'))
# print(list_instances())
# print(stop_instance('i-0690c6a84933f6d36'))
# print(terminate_instance('i-0c88d4f18a714ec3c'))
# print(create_instance())#i-0c88d4f18a714ec3c
# print(create_security_group())
# pprint(security_group())
# pprint(security_group_describe())
# print(security_group_delete('sg-0e1b133304da54096'))
print(security_group_ingress('sg-0c401604b521b7b91'))
