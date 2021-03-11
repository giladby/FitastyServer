import mysql.connector

class MySQLConnectionFields:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

def get_db_fields():
    host = "3.142.151.208"
    user = "admin"
    password = "epsilonEP2"
    database = "fitasty"
    return MySQLConnectionFields(host, user, password, database)

def get_mysql_connection(mysql_fields):
    return mysql.connector.connect(
        host=mysql_fields.host,
        user=mysql_fields.user,
        passwd=mysql_fields.password,
        database=mysql_fields.database)

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def handle_error():
    print("Error trying access mysql records")

def get_query(cursor):
    try:
        cursor.execute("SELECT * FROM users")
        for row in iter_row(cursor, 10):
            print(row)
    except:
        handle_error()

def close_connection(conn, cursor):
    if conn is not None:
        conn.close()
    if cursor is not None:
        cursor.close()

def get_mysql_cursor():
    conn = None
    cursor = None
    try:
        db_fields = get_db_fields()
        conn = get_mysql_connection(db_fields)
        cursor = conn.cursor()
    except:
       handle_error()
    return conn, cursor

def main():
    conn, cursor = get_mysql_cursor()
    get_query(cursor)
    close_connection(conn, cursor)

if __name__ == '__main__':
    main()