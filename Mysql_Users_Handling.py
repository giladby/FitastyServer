from Mysql_Connection_General import *

username_field_mysql = 'username'
password_field_mysql = 'password'
users_table_mysql = 'users'

def get_user_query(cursor, username, check_password, password):
    found = False
    error = False
    if cursor:
        try:
            query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql}='{username}'"
            if check_password:
                query += f" AND {password_field_mysql}='{password}'"
            cursor.execute(query)
            if cursor.fetchone():
                found = True
        except:
            error = True
    return found, error

def insert_user_query(conn, cursor, username, password):
    error = False
    if cursor:
        try:
            query = f"INSERT INTO {users_table_mysql} ({username_field_mysql}, {password_field_mysql}) VALUES (%s, %s)"
            val = (username, password)
            cursor.execute(query, val)
            conn.commit()
        except:
            error = True
    return error

def check_user(username, check_user, password):
    conn, cursor, error = get_mysql_cursor()
    result = None
    if not error:
        result, error = get_user_query(cursor, username, check_user, password)
    close_connection(conn, cursor)
    return result, error

def insert_user(username, password):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = insert_user_query(conn, cursor, username, password)
    close_connection(conn, cursor)
    return error