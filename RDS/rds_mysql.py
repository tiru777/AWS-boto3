import boto3
from pprint import pprint
import mysql.connector as mysql

rds_client = boto3.client('rds')


def create_database():
    response = rds_client.create_db_instance(
        DBName="sadguruvenamhards",
        DBInstanceIdentifier="sadguruvenamhards",
        AllocatedStorage=20,
        DBInstanceClass='db.t2.micro',
        Engine='MySQL',
        MasterUsername='admins',
        MasterUserPassword='password',
        Port=3306,
        EngineVersion='8.0.27',
        PubliclyAccessible=True,
        StorageType='gp2'
    )

    return response


def create_db():
    try:
        mydb = mysql.connect(
            host="endpoint",
            user="admin",
            password="Password"
        )

        cursor = mydb.cursor()

        cursor.execute("CREATE DATABASE aws_rds")
        # data = cursor.execute('show databases')

    except mysql.Error as e:
        print("Failed to create database {} ".format(e))


def check_db_connection():
    try:
        mydb = mysql.connect(
            host="endpoint",
            user="admin",
            password="Password",
            database="aws_rds"
        )

        print("Connection created",mydb)
        return mydb
    except mysql.Error as e:
        print("There is no connection {} ".format(e))


# create_db()
# check_db_connection()
def create_table():
    my_db = check_db_connection()
    cursor = my_db.cursor()
    cursor.execute("""create table Employee (
                                            Name varchar(20),
                                            age int,
                                            Address varchar(20))
                                            """
                   )
    print('table created')
    cursor.execute("show tables")
    for i in cursor:
        print(i)

# create_table()


def insert_data():
    mydb = check_db_connection()
    cursor = mydb.cursor()

    query = "INSERT INTO Employee(Name,age,Address) VALUES(%s,%s,%s)"
    values = ('thirumala',31,'reddy vari palli')
    cursor.execute(query,values)
    mydb.commit()

    cursor.execute('delete from Employee where Name="manu"')
    mydb.commit()
    # fetch
    cursor.execute('select * from Employee')
    data = cursor.fetchall()
    for i in data:
        print(i)
    print('table data inserted')


# insert_data()

def describe_data(db_name):
    response = rds_client.describe_db_instances(
        DBInstanceIdentifier=db_name
    )

    return response


pprint(describe_data("database-tiru-rds"))


def delete_db_instance(db_instance):
    response = rds_client.delete_db_instance(
        DBInstanceIdentifier=db_instance,
        SkipFinalSnapshot=False,
        FinalDBSnapshotIdentifier=db_instance+"snapshot",
        DeleteAutomatedBackups=True

    )

    return response


pprint(delete_db_instance('database-tiru-rds'))