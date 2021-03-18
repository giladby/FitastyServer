from Mysql_Connection_General import *
from Macros import *

def make_account_info_dict(mysql_user_record):
    return {f"{password_field_param}": mysql_user_record[password_field_mysql_position],
            f"{age_field_param}": mysql_user_record[age_field_mysql_position],
            f"{is_male_field_param}": mysql_user_record[is_male_field_mysql_position] == 1,
            f"{height_field_param}": mysql_user_record[height_field_mysql_position],
            f"{weight_field_param}": mysql_user_record[weight_field_mysql_position],
            f"{activity_factor_field_param}": mysql_user_record[activity_factor_field_mysql_position],
            f"{diet_type_field_param}": {f"{diet_type_carb_field_param}":
                                             mysql_user_record[diet_type_carb_field_mysql_position],
                                         f"{diet_type_fat_field_param}":
                                             mysql_user_record[diet_type_fat_field_mysql_position],
                                         f"{diet_type_protein_field_param}":
                                             mysql_user_record[diet_type_protein_field_mysql_position]},
            f"{weight_goal_field_param}": mysql_user_record[weight_goal_field_mysql_position]}

def get_account_info_query(cursor, username):
    found = False
    query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql}='{username}'"

    error, result = mysql_getting_single_action(cursor, query)
    if not error and result:
        found = True
        result = make_account_info_dict(result)

    return error, found, result

def check_user_query(cursor, username, check_password, password):
    found = False
    query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql}='{username}'"
    if check_password:
        query += f" AND {password_field_mysql}='{password}'"

    error, result = mysql_getting_single_action(cursor, query)
    if result:
        found = True

    return found, error

def insert_user_query(conn, cursor, username, password, age, is_male, height,
                      weight, activity_factor, diet_type, weight_goal):
    query = f"INSERT INTO {users_table_mysql} ({username_field_mysql}," \
            f" {password_field_mysql}, {age_field_mysql}, {is_male_field_mysql}," \
            f" {height_field_mysql}, {weight_field_mysql}, {activity_factor_field_mysql}," \
            f" {diet_type_fat_field_mysql}, {diet_type_carb_field_mysql}," \
            f" {diet_type_protein_field_mysql}, {weight_goal_field_mysql}) VALUES" \
            f" (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (username, password, age, 1 if is_male else 0, height, weight, activity_factor,
           diet_type[diet_type_fat_field_param], diet_type[diet_type_carb_field_param],
           diet_type[diet_type_protein_field_param], weight_goal)

    return mysql_insertion_action(conn, cursor, query, val)

def update_user_query(conn, cursor, prev_username, username, password, age, is_male,
                      height, weight, activity_factor, diet_type, weight_goal):
    query = f"UPDATE {users_table_mysql} SET {username_field_mysql} = %s," \
            f" {password_field_mysql} = %s, {age_field_mysql} = %s," \
            f" {is_male_field_mysql} = %s, {height_field_mysql} = %s," \
            f" {weight_field_mysql} = %s, {activity_factor_field_mysql} = %s," \
            f" {diet_type_fat_field_mysql} = %s, {diet_type_carb_field_mysql} = %s," \
            f" {diet_type_protein_field_mysql} = %s, {weight_goal_field_mysql} = %s" \
            f" WHERE {username_field_mysql} = '{prev_username}'"
    val = (username, password, age, is_male, height, weight, activity_factor,
           diet_type[diet_type_fat_field_param], diet_type[diet_type_carb_field_param],
           diet_type[diet_type_protein_field_param], weight_goal)

    return mysql_insertion_action(conn, cursor, query, val)

def update_user(prev_username, username, password, age, is_male, height, weight,
                activity_factor, diet_type, weight_goal):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = update_user_query(conn, cursor, prev_username, username,
                                  password, age, is_male, height, weight,
                                  activity_factor, diet_type, weight_goal)
    close_connection(conn, cursor)
    return error

def check_user(username, check_user, password):
    conn, cursor, error = get_mysql_cursor()
    result = None
    if not error:
        result, error = check_user_query(cursor, username, check_user, password)
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

def get_account_info_by_username(username):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_account_info_query(cursor, username)
    close_connection(conn, cursor)
    return error, found, result

