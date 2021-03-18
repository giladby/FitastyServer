from Mysql_Connection_General import *

username_field_mysql = 'username'
password_field_mysql = 'password'
age_field_mysql = 'age'
is_male_field_mysql = 'is_male'
height_field_mysql = 'height'
weight_field_mysql = 'weight'
activity_factor_field_mysql = 'activity_factor'
weight_goal_field_mysql = 'weight_goal'
diet_type_carb_field_mysql = 'diet_type_carb'
diet_type_fat_field_mysql = 'diet_type_fat'
diet_type_protein_field_mysql = 'diet_type_protein'
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

def insert_user_query(conn, cursor, username, password, age,
                      is_male, height, weight, activity_factor,
                      diet_type, weight_goal):
    error = False
    if cursor:
        try:
            query = f"INSERT INTO {users_table_mysql} ({username_field_mysql}," \
                    f" {password_field_mysql}, {age_field_mysql}, {is_male_field_mysql}," \
                    f" {height_field_mysql}, {weight_field_mysql}, {activity_factor_field_mysql}," \
                    f" {diet_type_fat_field_mysql}, {diet_type_carb_field_mysql}," \
                    f" {diet_type_protein_field_mysql}, {weight_goal_field_mysql}) VALUES" \
                    f" (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (username, password, age, is_male, height, weight, activity_factor,
                   diet_type[0], diet_type[1], diet_type[2], weight_goal)
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

def insert_user(username, password, age, is_male, height, weight,
                activity_factor, diet_type, weight_goal):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = isinstance(diet_type, list) and len(diet_type) == 3
    if not error:
        error = insert_user_query(conn, cursor, username, password, age,
                                  is_male, height, weight, activity_factor,
                                  diet_type, weight_goal)
    close_connection(conn, cursor)
    return error