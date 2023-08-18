import boto3
import json

iam = boto3.client('iam')


# user


def iam_client():
    # Create IAM client # TODO: while calling this function its not working
    iam = boto3.client('iam')
    return iam


def list_users():
    # List users with the pagination interface
    paginator = iam.get_paginator('list_users')
    for response in paginator.paginate():
        return response


def update_user_name(old_user_name,new_usr_name):
    # Create IAM client
    # Update a user name
    data = iam.update_user(
        UserName=old_user_name,
        NewUserName=new_usr_name
    )
    return data
    # to check after update call list user


def create_user(name):
    """

    :param name: user name :return:
    """
    response = iam.create_user(
        UserName=name
    )
    return response


# create_user('manu')


def delete_user(user_name):
    # after deleting access key of a user then only it will be possible for deletion
    # Delete a user
    data = iam.delete_user(
        UserName=user_name
    )
    return data


# delete_user('manu')


# Policies

def get_policy(arn):
    """
    get policy using policy arn
    """
    response = iam.get_policy(
        PolicyArn= arn
    )

    return response


def list_policies():
    # List policies with the pagination interface
    policies = {}
    paginator = iam.get_paginator('list_policies')
    for response in paginator.paginate(Scope="AWS"):
        count = 0
        for policy in response["Policies"]:
            policies[count] = policy
            count = count + 1
        # policies = policy["PolicyName"]
        # arn = policy['Arn']
    return policies


def attach_policy(policy_arn, username):
    """

    :param policy_arn: arn:aws:iam::aws:policy/AmazonRDSFullAccess
    :param username: manu
    :return: status 200
    """

    response = iam.attach_user_policy(
        UserName=username,
        PolicyArn=policy_arn
    )

    return response


def detach_policy(policy_arn, username):
    """

    :param policy_arn: arn:aws:iam::aws:policy/AmazonRDSFullAccess
    :param username: manu
    :return: status 200
    """

    response = iam.detach_user_policy(
        UserName=username,
        PolicyArn=policy_arn
    )

    return response


# print(detach_policy("arn:aws:iam::aws:policy/AmazonRDSFullAccess", "manu"))


def create_custom_policy():
    """
    creating custom policy with allowing all policies and attach to user
    """

    user_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*"
            }
        ]
    }

    response = iam.create_policy(
        PolicyName='tirufullaccess',
        PolicyDocument=json.dumps(user_policy)
    )

    return response


def create_group(group_name):
    """

    :param group_name: EX EC2 access group
    :return: NA
    """
    iam.create_group(GroupName=group_name)


def delete_group(group_name):
    """

    :param group_name: string
    :return:
    """
    iam.delete_group(GroupName=group_name)


# delete_group("EC2Access")


def attach_group_policy(policy_arn, group_name):
    """

    :param policy_arn: Example EC2 ARN ==> arn:aws:iam::aws:policy/AmazonEC2FullAccess
    :param group_name: created EC2 access group name
    :return: response
    """

    response = iam.attach_group_policy(
        GroupName=group_name,
        PolicyArn=policy_arn
    )

    return response


# print(attach_group_policy('arn:aws:iam::aws:policy/AmazonEC2FullAccess', 'EC2Access'))

def add_user_to_group(username, group_name):
    response = iam.add_user_to_group(
        UserName=username,
        GroupName=group_name
    )

    return response


# print(add_user_to_group('manu', 'EC2Access'))


def detach_group_policy(policy_arn, group_name):
    """

    :param policy_arn: Example EC2 ARN ==> arn:aws:iam::aws:policy/AmazonEC2FullAccess
    :param group_name: created EC2 access group name
    :return: response
    """

    response = iam.detach_group_policy(
        GroupName=group_name,
        PolicyArn=policy_arn
    )

    return response


# print(detach_group_policy("arn:aws:iam::aws:policy/AmazonEC2FullAccess","EC2Access"))


def delete_user_group(username, group_name):
    iam = boto3.resource('iam')  # removing user from group
    group = iam.Group(group_name)

    response = group.remove_user(
        UserName=username
    )

    return response


# delete_user_group('manu', 'EC2Access')


def create_access(username):
    response = iam.create_access_key(
        UserName=username
    )

    return response


# print(create_access('manu'))


def update_access(access_key):
    iam.update_access_key(
        AccessKeyId=access_key,
        Status='Inactive',
        UserName='manu'

    )


# update_access()

def delete_access(access_key):
    iam.delete_access_key(
        AccessKeyId=access_key,
        UserName='manu'

    )


# delete_access()


def create_login_credentials_console(username,password):
    """

    :param username: username
    :return: already created user with program or console of programmatic user and we can create console access
    """
    login_profile = iam.create_login_profile(
        Password=password,
        PasswordResetRequired=False,  # after login reset purpose used
        UserName=username
    )

    return login_profile


# create_login_credentials_console('manu')


def delete_login_credentials_console(username):
    """

    :param username: username
    :return: already created user with program or console of programmatic user and we can delete console access before
    deleting username
    """
    login_profile = iam.delete_login_profile(
        UserName=username
    )

    return login_profile

# delete_login_credentials_console('manu')
