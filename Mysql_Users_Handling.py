from Mysql_Connection_General import *
from Macros import *
from Utils import *

def make_account_info_dict(mysql_user_record):
    return {f"{password_field_param}": mysql_user_record[password_field_mysql],
            f"{age_field_param}": mysql_user_record[age_field_mysql],
            f"{is_male_field_param}": mysql_user_record[is_male_field_mysql] == 1,
            f"{height_field_param}": mysql_user_record[height_field_mysql],
            f"{weight_field_param}": mysql_user_record[weight_field_mysql],
            f"{activity_factor_field_param}": mysql_user_record[activity_factor_field_mysql],
            f"{diet_type_field_param}": {f"{diet_type_fat_field_param}":
                                             mysql_user_record[diet_type_fat_field_mysql],
                                         f"{diet_type_carb_field_param}":
                                             mysql_user_record[diet_type_carb_field_mysql],
                                         f"{diet_type_protein_field_param}":
                                             mysql_user_record[diet_type_protein_field_mysql]},
            f"{weight_goal_field_param}": mysql_user_record[weight_goal_field_mysql]}

def calc_calorie_info(age, is_male, height, weight, activity_factor, diet_type_fat,
                      diet_type_carb, diet_type_protein, weight_goal):
    calorie_to_reduce_for_single_kg = 7716
    days_in_week = 7
    fiber_grams_per_1000kg = 14
    calories_per_single_fat_gram = 9
    calories_per_single_carb_gram = 4
    calories_per_single_protein_gram = 4

    bmr = 10 * weight + 6.25 * height - 5 * age
    if is_male:
        bmr += 5
    else:
        bmr -= 161

    calorie_goal = (bmr * activity_factor) + ((weight_goal * calorie_to_reduce_for_single_kg) / days_in_week)

    fat = calorie_goal * diet_type_fat / calories_per_single_fat_gram
    carb = calorie_goal * diet_type_carb / calories_per_single_carb_gram
    fiber = calorie_goal * fiber_grams_per_1000kg / 1000
    protein = calorie_goal * diet_type_protein / calories_per_single_protein_gram

    return fat, carb, fiber, protein

def make_calorie_info_dict(mysql_user_record):
    age = mysql_user_record[age_field_mysql]
    is_male = mysql_user_record[is_male_field_mysql] == 1
    height = mysql_user_record[height_field_mysql]
    weight = mysql_user_record[weight_field_mysql]
    activity_factor = mysql_user_record[activity_factor_field_mysql]
    diet_type_fat = mysql_user_record[diet_type_fat_field_mysql]
    diet_type_carb = mysql_user_record[diet_type_carb_field_mysql]
    diet_type_protein = mysql_user_record[diet_type_protein_field_mysql]
    weight_goal = mysql_user_record[weight_goal_field_mysql]

    fat, carb, fiber, protein = calc_calorie_info(age, is_male, height, weight, activity_factor, diet_type_fat,
                                                  diet_type_carb, diet_type_protein, weight_goal)
    return {f"{fat_field_param}": fat,
            f"{carb_field_param}": carb,
            f"{fiber_field_param}": fiber,
            f"{protein_field_param}": protein}

def get_account_info_query(cursor, username):
    found = False
    query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql}='{username}'"

    error, result = mysql_getting_action(cursor, query, True)
    if not error and result:
        found = True
        result = make_account_info_dict(result)

    return error, found, result

def get_calorie_info_query(cursor, username):
    found = False
    query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql}='{username}'"

    error, result = mysql_getting_action(cursor, query, True)
    if not error and result:
        found = True
        result = make_calorie_info_dict(result)

    return error, found, result

def delete_user_query(cursor, username):
    query = f"DELETE FROM {users_table_mysql} WHERE {username_field_mysql} = %s"
    val = (username, )

    return mysql_single_action(cursor, query, val)

def insert_user_query(cursor, username, password, age, is_male, height,
                      weight, activity_factor, diet_type, weight_goal):
    query = f"INSERT INTO {users_table_mysql} ({username_field_mysql}," \
            f" {password_field_mysql}, {age_field_mysql}, {is_male_field_mysql}," \
            f" {height_field_mysql}, {weight_field_mysql}, {activity_factor_field_mysql}," \
            f" {diet_type_fat_field_mysql}, {diet_type_carb_field_mysql}," \
            f" {diet_type_protein_field_mysql}, {weight_goal_field_mysql}) VALUES" \
            f" (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (username, password, age, convert_boolean_to_number(is_male), height, weight, activity_factor,
           diet_type[diet_type_fat_field_param], diet_type[diet_type_carb_field_param],
           diet_type[diet_type_protein_field_param], weight_goal)

    return mysql_single_action(cursor, query, val)

def update_user_query(cursor, prev_username, username, password, age, is_male,
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

    return mysql_single_action(cursor, query, val)

def update_user(prev_username, username, password, age, is_male, height, weight,
                activity_factor, diet_type, weight_goal):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = update_user_query(cursor, prev_username, username,
                                  password, age, is_male, height, weight,
                                  activity_factor, diet_type, weight_goal)
    close_connection(conn, cursor)
    return error

def check_user(username, check_user, password):
    query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql}='{username}'"
    if check_user:
        query += f" AND {password_field_mysql}='{password}'"
    return check_existing(query)

def insert_user(username, password, age, is_male, height, weight,
                activity_factor, diet_type, weight_goal):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = isinstance(diet_type, list) and len(diet_type) == 3
    if not error:
        error = insert_user_query(cursor, username, password, age,
                                  is_male, height, weight, activity_factor,
                                  diet_type, weight_goal)
    close_connection(conn, cursor)
    return error

def delete_user(username):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = delete_user_query(cursor, username)
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

def get_calorie_info_by_username(username):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_calorie_info_query(cursor, username)
    close_connection(conn, cursor)
    return error, found, result

