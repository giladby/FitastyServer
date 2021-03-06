from Mysql_Connection_General import *
from Macros import *
from Utils import *
from Mysql_Diet_Diaries_Handling import delete_diet_diary_transaction_func
from Machine_Learning import *

# ======================================================================================================================
# get_account_info QUERY

def make_account_info_dict(mysql_user_record):
    return {f"{password_field_param}": mysql_user_record[password_field_mysql],
            f"{age_field_param}": mysql_user_record[age_field_mysql],
            f"{is_male_field_param}": mysql_user_record[is_male_field_mysql] == 1,
            f"{height_field_param}": mysql_user_record[height_field_mysql],
            f"{weight_field_param}": mysql_user_record[weight_field_mysql],
            f"{country_field_param}": mysql_user_record[country_field_mysql],
            f"{activity_factor_field_param}": mysql_user_record[activity_factor_field_mysql],
            f"{diet_type_field_param}": {f"{diet_type_fat_field_param}":
                                         mysql_user_record[diet_type_fat_field_mysql],
                                         f"{diet_type_carb_field_param}":
                                         mysql_user_record[diet_type_carb_field_mysql],
                                         f"{diet_type_protein_field_param}":
                                         mysql_user_record[diet_type_protein_field_mysql]},
            f"{weight_goal_field_param}": mysql_user_record[weight_goal_field_mysql],
            f"{is_vegan_field_param}": mysql_user_record[is_vegan_field_mysql] == 1,
            f"{is_vegetarian_field_param}": mysql_user_record[is_vegetarian_field_mysql] == 1,
            f"{is_lactose_free_field_param}": mysql_user_record[is_lactose_free_field_mysql] == 1,
            f"{is_gluten_free_field_param}": mysql_user_record[is_gluten_free_field_mysql] == 1}

def get_account_info_query(cursor, username):
    found = False
    query = f"SELECT * FROM {users_table_mysql} JOIN {countries_table_mysql}" \
            f" ON {users_table_mysql}.{country_id_field_mysql} = {countries_table_mysql}.{id_field_mysql}" \
            f" WHERE {username_field_mysql} = %s"
    val = (username,)
    error, result = mysql_getting_action(cursor, query, val, True)
    if not error and result:
        found = True
        result = make_account_info_dict(result)

    return error, found, result

def get_account_info_by_username(username):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_account_info_query(cursor, username)
    close_connection(conn, cursor)
    return error, found, result

# ======================================================================================================================
# get_calorie_info QUERY

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

def get_calorie_info_query(cursor, username):
    found = False
    query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql} = %s"
    val = (username,)
    error, result = mysql_getting_action(cursor, query, val, True)
    if not error and result:
        found = True
        result = make_calorie_info_dict(result)

    return error, found, result

def get_calorie_info_by_username(username):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_calorie_info_query(cursor, username)
    close_connection(conn, cursor)
    return error, found, result

# ======================================================================================================================
# delete_user QUERY

def delete_user_main_transaction_func(cursor, user_id):
    query = f"DELETE FROM {users_table_mysql} WHERE {id_field_mysql} = %s"
    val = (user_id, )
    cursor.execute(query, val)

def delete_user_transaction_func(cursor, user_id):
    delete_diet_diary_transaction_func(cursor, (None, user_id, True))
    delete_user_main_transaction_func(cursor, user_id)

def delete_user_query(conn, cursor, user_id):
    return transaction_execute(conn, cursor, delete_user_transaction_func, user_id)

def delete_user(user_id):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = delete_user_query(conn, cursor, user_id)
    close_connection(conn, cursor)
    return error

# ======================================================================================================================
# insert_user QUERY

def get_country_id(cursor, country):
    found = False
    query = f"SELECT {id_field_mysql} FROM {countries_table_mysql} WHERE {country_field_mysql} = %s"
    val = (country,)
    error, result = mysql_getting_action(cursor, query, val, True)
    if not error and result:
        found = True
        result = result[id_field_mysql]
    error = error or not found
    return error, result

def insert_user_query(cursor, username, password, age, is_male, height,
                      weight, activity_factor, diet_type, weight_goal, country, is_vegan,
                      is_vegetarian, is_lactose_free, is_gluten_free):
    query = f"INSERT INTO {users_table_mysql}" \
            f" ({username_field_mysql}," \
            f" {password_field_mysql}, {age_field_mysql}, {is_male_field_mysql}," \
            f" {height_field_mysql}, {weight_field_mysql}, {activity_factor_field_mysql}," \
            f" {diet_type_fat_field_mysql}, {diet_type_carb_field_mysql}," \
            f" {diet_type_protein_field_mysql}, {weight_goal_field_mysql}, {country_id_field_mysql}," \
            f" {is_vegan_field_mysql}, {is_vegetarian_field_mysql}, {is_lactose_free_field_mysql}," \
            f" {is_gluten_free_field_mysql})" \
            f" SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, {countries_table_mysql}.{id_field_mysql}," \
            f" %s, %s, %s, %s" \
            f" FROM {countries_table_mysql}" \
            f" WHERE {countries_table_mysql}.{country_field_mysql} = %s"
    val = (username, password, age, convert_boolean_to_number(is_male), height, weight,
           activity_factor, diet_type[diet_type_fat_field_param],
           diet_type[diet_type_carb_field_param], diet_type[diet_type_protein_field_param],
           weight_goal, convert_boolean_to_number(is_vegan), convert_boolean_to_number(is_vegetarian),
           convert_boolean_to_number(is_lactose_free), convert_boolean_to_number(is_gluten_free), country)

    return mysql_single_action(cursor, query, val)

def insert_user(username, password, age, is_male, height, weight,
                activity_factor, diet_type, weight_goal, country, is_vegan,
                is_vegetarian, is_lactose_free, is_gluten_free):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = isinstance(diet_type, list) and len(diet_type) == 3
    if not error:
        error = insert_user_query(cursor, username, password, age,
                                  is_male, height, weight, activity_factor,
                                  diet_type, weight_goal, country, is_vegan,
                                  is_vegetarian, is_lactose_free, is_gluten_free)
    close_connection(conn, cursor)
    return error

# ======================================================================================================================
# update_user QUERY

def update_user_query(cursor, prev_username, username, password, age, is_male,
                      height, weight, activity_factor, diet_type, weight_goal, country, is_vegan,
                      is_vegetarian, is_lactose_free, is_gluten_free):
    query = f"UPDATE {users_table_mysql}" \
            f" SET {username_field_mysql} = %s," \
            f" {password_field_mysql} = %s, {age_field_mysql} = %s," \
            f" {is_male_field_mysql} = %s, {height_field_mysql} = %s, {weight_field_mysql} = %s," \
            f" {country_id_field_mysql} =" \
            f" (SELECT {id_field_mysql} FROM {countries_table_mysql} WHERE {country_field_mysql} = %s)," \
            f" {activity_factor_field_mysql} = %s," \
            f" {diet_type_fat_field_mysql} = %s, {diet_type_carb_field_mysql} = %s," \
            f" {diet_type_protein_field_mysql} = %s, {weight_goal_field_mysql} = %s," \
            f" {is_gluten_free_field_mysql} = %s, {is_vegan_field_mysql} = %s," \
            f" {is_vegetarian_field_mysql} = %s, {is_lactose_free_field_mysql} = %s"  \
            f" WHERE {username_field_mysql} = '{prev_username}'"
    val = (username, password, age, convert_boolean_to_number(is_male), height, weight, country, activity_factor,
           diet_type[diet_type_fat_field_param], diet_type[diet_type_carb_field_param],
           diet_type[diet_type_protein_field_param], weight_goal,
           convert_boolean_to_number(is_gluten_free), convert_boolean_to_number(is_vegan),
           convert_boolean_to_number(is_vegetarian), convert_boolean_to_number(is_lactose_free))

    return mysql_single_action(cursor, query, val)

def update_user(prev_username, username, password, age, is_male, height, weight,
                activity_factor, diet_type, weight_goal, country, is_vegan,
                is_vegetarian, is_lactose_free, is_gluten_free):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = update_user_query(cursor, prev_username, username,
                                  password, age, is_male, height, weight,
                                  activity_factor, diet_type, weight_goal, country, is_vegan,
                                  is_vegetarian, is_lactose_free, is_gluten_free)
    close_connection(conn, cursor)
    return error

# ======================================================================================================================
# check_user QUERY

def check_user(username, check_user, password):
    query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql} = %s"
    val = (username,)
    if check_user:
        query += f" AND {password_field_mysql} = %s"
        val += (password,)
    result, found, error = check_existing(query, val)
    result = result[id_field_mysql] if not error and found else None
    return result,found, error

# ======================================================================================================================
# get_countries QUERY

def get_countries_query(cursor):
    countries = []

    query = f"SELECT {country_field_mysql} FROM {countries_table_mysql}"

    error, result = mysql_get_data(cursor, query, False)
    if not error and result:
        for record in result:
            countries.append(record[country_field_mysql])
        result = {f"{countries_field_param}": countries}

    return error, result

def get_countries():
    result = None
    conn, cursor, error = get_mysql_cursor()
    get_last_record(cursor,None)
    if not error:
        error, result = get_countries_query(cursor)
    close_connection(conn, cursor)
    return error, result