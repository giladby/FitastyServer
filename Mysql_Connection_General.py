import mysql.connector

class MySQLConnectionFields:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

def close_connection(conn, cursor):
    if conn is not None:
        conn.close()
    if cursor is not None:
        cursor.close()

def get_mysql_cursor():
    conn = None
    cursor = None
    error = False
    try:
        db_fields = get_db_fields()
        conn = get_mysql_connection(db_fields)
        cursor = conn.cursor()
    except:
       error = True
    return conn, cursor, error

def iter_row(cursor, size=10):
    #running example:
    #cursor.execute("SELECT * FROM users")
    #    for row in iter_row(cursor, 10):
    #        print(row)
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def get_db_fields():
    host = "fitasty-db.cc4qtocqbg7k.us-east-2.rds.amazonaws.com"
    host = "127.0.0.1"
    user = "admin"
    user = "root"
    password = "epsilonEP2"
    password = "123456"
    database = "fitasty"
    database = "fitasty_demo"
    return MySQLConnectionFields(host, user, password, database)

def get_mysql_connection(mysql_fields):
    return mysql.connector.connect(
        host=mysql_fields.host,
        user=mysql_fields.user,
        passwd=mysql_fields.password,
        database=mysql_fields.database)