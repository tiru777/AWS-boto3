from pprint import pprint

import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key

db_client = boto3.client('dynamodb')
db = boto3.resource('dynamodb')


# create table


def list_tables_db():
    response = db_client.list_tables()

    return response['TableNames']


def create_table():
    # key type == Hash for partition key and range for sort key
    table = db.create_table(
        TableName='Employee2',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },

            {
                'AttributeName': 'Name',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'Name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    return table


def update_table(table_name):
    response = db_client.update_table(
        TableName=table_name,
        BillingMode='PROVISIONED',

        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    return response


def describing_table(table_name):
    """
    describes the information of the table
    """
    return db_client.describe_table(TableName=table_name)


def insert_item_resource_lib(table_name):
    table = db.Table(table_name)

    dt = table.put_item(
        Item={
            'id': 1,
            'Name': "Parwiz",
            'age': 28
        }
    )
    return dt


def insert_item_resource_batch(table_name):
    table = db.Table(table_name)

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'id': 3,
                'Name': "manu",
                'age': 28
            }
        )
        batch.put_item(
            Item={
                'id': 4,
                'Name': "madhu",
                'age': 28
            }
        )


def insert_item_client(table_name):
    dt = db_client.put_item(
        TableName=table_name,
        Item={
            'id': {'N': '2'},
            'Name': {'S': 'tiru'},
            'age': {'N': '28'}
        }
    )
    return dt


def backup_table_create(table_name):
    response = db_client.create_backup(
        TableName=table_name,
        BackupName=table_name + 'backup'
    )

    return response


def backup_table_delete(arn_backup):
    response = db_client.delete_backup(
        BackupArn=arn_backup
    )

    return response


def delete_table(table_name):
    # todo: check how to delete with resource lib
    response = db_client.delete_table(
        TableName=table_name
    )

    return response


def get_item_attributes_lib_res(table_name):
    """
    if table contains both partition key and sort key,
    we have to specify both to get item
    """
    '''
    table = db.Table(table_name)
    response = table.get_item(
        Key={
            'id':2,
            'Name': 'tiru',
        }
    )
    '''
    response = db_client.get_item(
        TableName=table_name,
        Key={
            'id': {'N': '2'},
            'Name': {'S': 'tiru'}
        }
    )
    # print("response:", response)
    return response['Item']


def get_item_batch(table_name):
    response = db.batch_get_item(
        RequestItems={
            table_name: {
                'Keys': [
                    {
                        'id': 2,
                        'Name': 'tiru'

                    },
                    {
                        'id': 3,
                        'Name': 'manu'
                    },
                ]
            }
        }
    )

    return response['Responses']


def scan(table_name):
    """get all data"""

    '''    table = db.Table(table_name)

    response = table.scan()'''
    response = db_client.scan(TableName=table_name)

    return response['Items']


def json_file_insert(json_file, table_name):
    """
    insert data of a json file
    """
    with open(json_file) as fp:
        movie_list = json.load(fp, parse_float=Decimal)
        table = db.Table(table_name)

        for movie in movie_list:
            year = int(movie['year'])
            title = movie['title']
            print("Adding movie : ", year, title)
            table.put_item(Item=movie)


def get_movie(table_name, year, title):
    table = db.Table(table_name)
    response = table.get_item(
        Key={
            'year': year,
            'title': title,
        }
    )
    return response


def update_movie(title, year, rating, plot, dynamodb=None):
    # todo : practice
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Movies')

    response = table.update_item(
        Key={
            'year': year,
            'title': title
        },
        UpdateExpression="set info.rating=:r, info.plot=:p",
        ExpressionAttributeValues={
            ':r': Decimal(rating),
            ':p': plot,
        },

        ReturnValues='UPDATED_NEW'
    )

    return response


def delete_item(table_name, year, title):
    table = db.Table(table_name)
    table.delete_item(
        Key={
            'year': year,
            'title': title
        }
    )


def query_key(table_name, year):
    table = db.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('year').eq(year)
    )

    return response['Items']


# data = create_table()
# data = insert_item_client('Employee')
# data = delete_table("Employee2")
# data = insert_item("Employee")
# data = list_tables_db()
# data = update_table('Employee')
# data = describing_table('Employee')
# insert_item_resource_batch('Employee')
# data = backup_table_create('Employee')
# data = backup_table_delete
# ('arn:aws:dynamodb:ap-southeast-2:647047433851:table/Employee/backup/01692193850786-f2616932')
# data = get_item_attributes_lib_res('Employee')
# data = get_item_batch('Employee')
# data = scan('Employee')
# data = json_file_insert('moviedata.json', 'Movies')
# data = get_movie("Movies",2013,'This Is the End')
# data = delete_item("Movies",2013,'This Is the End')
# update_response = update_movie(
#         "The Shawshank Redemption", 1994, "5.4", "This is just for testing"
#     )
data = query_key('Movies', 2013)

print(pprint(data))
