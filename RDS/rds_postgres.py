import psycopg2


def check_connection():
    try:
        conn = psycopg2.connect(
            database="mydb",
            user="postgres",
            password="password",
            host="endpoint",
            port=5432
        )
        conn.autocommit = True
        print("Database connected")
        return conn
    except Exception as arg:
        print("Failed to connect the database", arg)


def postgres_methods():
    try:
        conn = check_connection()
        mycursor = conn.cursor()
        query = "CREATE DATABASE mydb"
        mycursor.execute(query)
        print("Database created")

        # create table
        query = "CREATE TABLE Employee (ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, EMAIL TEXT NOT NULL)"
        mycursor.execute(query)
        conn.commit()
        print("Table created")

        # insert table
        query = "INSERT INTO Employee (ID, NAME, EMAIL) VALUES (1, 'parwiz', 'par@gmail.com')"
        mycursor.execute(query)
        conn.commit()
        print("Data has been added")

        # fetch
        query = "SELECT * FROM Employee"
        mycursor.execute(query)
        rows = mycursor.fetchall()
        for data in rows:
            print(data)

        # delete
        query = "DELETE FROM Employee WHERE id=1"
        mycursor.execute(query)
        conn.commit()
        print("Data deleted")

    except Exception as arg:
        print("Failed to create database", arg)
