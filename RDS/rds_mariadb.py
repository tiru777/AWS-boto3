import mariadb


def check_connection():
    try:
        db = mariadb.connect(
            host="endpoint",
            user="admin",
            password="password",
            database="mydbexample"

        )
        cur = db.cursor()
        print("There is a connection with the database")
        return cur
    except mariadb.Error as e:
        print("There is not any connection {} ".format(e))


def maria_db_usage():
    cur = check_connection()
    cur.execute("CREATE TABLE Person (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),lastname VARCHAR(255) )")
    print("Table created ")


