import mysql.connector
from Macros import *

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
        cursor = conn.cursor(dictionary=True)
    except:
       error = True
    return conn, cursor, error

def get_db_fields():
    return MySQLConnectionFields(mysql_host, mysql_user, mysql_password, mysql_database)

def get_mysql_connection(mysql_fields):
    return mysql.connector.connect(
        host=mysql_fields.host,
        user=mysql_fields.user,
        passwd=mysql_fields.password,
        database=mysql_fields.database,
        autocommit=True)

def mysql_single_action(cursor, query, val):
    error = False
    if cursor:
        try:
            cursor.execute(query, val)
        except:
            error = True
    return error

def multiple_action_body_func(cursor, args):
    actions_arr = args[0]

    for action in actions_arr:
        query = action[0]
        val = action[1]
        cursor.execute(query, val)

def transaction_execute(conn, cursor, body_func, args):
    error = False
    if cursor:
        try:
            conn.start_transaction()
            body_func(cursor, args)
            conn.commit()
        except:
            conn.rollback()
            error = True
    return error

def mysql_multiple_action(conn, cursor, actions_arr):
    return transaction_execute(conn,cursor, multiple_action_body_func, (actions_arr, ))

def mysql_getting_action(cursor, query, val, single):
    result = None
    error = False
    if cursor:
        try:
            cursor.execute(query, val)
            if single:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        except:
            error = True
    return error, result

def check_query(cursor, checking_query, val):
    found = False

    error, result = mysql_getting_action(cursor, checking_query, val, True)
    if result:
        found = True

    return result, found, error

def check_existing(checking_query, val):
    conn, cursor, error = get_mysql_cursor()
    result = None
    found = False
    if not error:
        result, found, error = check_query(cursor, checking_query, val)
    close_connection(conn, cursor)
    return result, found, error