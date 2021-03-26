from Mysql_Connection_General import *
from Macros import *
from Utils import *

def make_dish_info_dict(dish_name, mysql_user_records):
    fat = 0
    carb = 0
    fiber = 0
    protein = 0
    ingredients_arr = []

    for record in mysql_user_records:
        fat += record[fat_field_mysql]
        carb += record[carb_field_mysql]
        fiber += record[fiber_field_mysql]
        protein += record[protein_field_mysql]
        ingredient_list = {f"{ingredient_name_field_param}": record[ingredient_name_field_mysql],
                           f"{is_liquid_field_param}": record[is_liquid_field_mysql],
                           f"{ingredient_amount_field_param}": record[ingredient_amount_field_mysql]}
        ingredients_arr.append(ingredient_list)

    return {f"{dish_name_field_param}": dish_name,
            f"{fat_field_param}": fat,
            f"{carb_field_param}": carb,
            f"{fiber_field_param}": fiber,
            f"{protein_field_param}": protein,
            f"{ingredient_name_field_param}": ingredients_arr}

def get_dish_info_query(cursor, dish_name):
    found = False
    query = f"SELECT * FROM {dish_ingredients_table_mysql} JOIN {food_ingredients_table_mysql}" \
            f" ON ({dish_ingredients_table_mysql}.{ingredient_name_field_mysql} =" \
            f" {food_ingredients_table_mysql}.{ingredient_name_field_mysql})" \
            f" WHERE {dish_name_field_mysql} = '{dish_name}'"

    error, result = mysql_getting_action(cursor, query, False)
    if not error and result:
        found = True
        result = make_dish_info_dict(dish_name, result)

    return error, found, result

def make_ingredient_info_dict(mysql_user_record):
    return {f"{ingredient_name_field_param}": mysql_user_record[ingredient_name_field_mysql],
            f"{is_liquid_field_param}": mysql_user_record[is_liquid_field_mysql] == 1,
            f"{fat_field_param}": mysql_user_record[fat_field_mysql],
            f"{carb_field_param}": mysql_user_record[carb_field_mysql],
            f"{fiber_field_param}": mysql_user_record[fiber_field_mysql],
            f"{protein_field_param}": mysql_user_record[protein_field_mysql],
            f"{is_vegan_field_param}": mysql_user_record[is_vegan_field_mysql] == 1,
            f"{is_vegetarian_field_param}": mysql_user_record[is_vegetarian_field_mysql] == 1,
            f"{is_gluten_free_field_param}": mysql_user_record[is_gluten_free_field_mysql] == 1,
            f"{is_lactose_free_field_param}": mysql_user_record[is_lactose_free_field_mysql] == 1,
            f"{serving_size_field_param}": mysql_user_record[serving_size_field_mysql]}

def get_ingredient_info_query(cursor, ingredient_name):
    found = False
    query = f"SELECT * FROM {food_ingredients_table_mysql} WHERE {ingredient_name_field_mysql}='{ingredient_name}'"

    error, result = mysql_getting_action(cursor, query, True)
    if not error and result:
        found = True
        result = make_ingredient_info_dict(result)

    return error, found, result

def insert_ingredient_query(cursor, name, is_liquid, fat, carbs, fiber, protein,
                            is_vegan, is_vegetarian,is_gluten_free,
                            is_lactose_free, serving):
    query = f"INSERT INTO {food_ingredients_table_mysql} ({ingredient_name_field_mysql}," \
            f" {is_liquid_field_mysql}, {fat_field_mysql}, {carb_field_mysql}," \
            f" {fiber_field_mysql}, {protein_field_mysql}, {is_vegan_field_mysql}," \
            f" {is_vegetarian_field_mysql}, {is_gluten_free_field_mysql}," \
            f" {is_lactose_free_field_mysql}, {serving_size_field_mysql}) VALUES" \
            f" (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, convert_boolean_to_number(is_liquid), fat, carbs, fiber, protein,
           convert_boolean_to_number(is_vegan), convert_boolean_to_number(is_vegetarian),
           convert_boolean_to_number(is_gluten_free),
           convert_boolean_to_number(is_lactose_free), serving)

    return mysql_single_action(cursor, query, val)

def get_filtered_foods_query(cursor, begin_name,max_fat, max_carb, max_fiber,
                             max_protein, min_fat, min_carb, min_fiber,
                             min_protein, is_vegan, is_vegetarian,
                             is_lactose_free, is_gluten_free, include_dish, include_ingredient):
    return ""

def get_filtered_foods(begin_name,max_fat, max_carb, max_fiber,
                       max_protein, min_fat, min_carb, min_fiber,
                       min_protein, is_vegan, is_vegetarian,
                       is_lactose_free, is_gluten_free, include_dish, include_ingredient):
    result = None
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, result = get_filtered_foods_query(cursor, begin_name,max_fat, max_carb, max_fiber,
                                                 max_protein, min_fat, min_carb, min_fiber,
                                                 min_protein, is_vegan, is_vegetarian,
                                                 is_lactose_free, is_gluten_free,
                                                 include_dish, include_ingredient)
    close_connection(conn, cursor)
    return error, result

def check_ingredient(ingredient_name):
    checking_query = f"SELECT * FROM {food_ingredients_table_mysql} WHERE" \
                     f" {ingredient_name_field_mysql}='{ingredient_name}'"
    return check_existing(checking_query)

def check_dish(dish_name):
    checking_query = f"SELECT * FROM {dishes_table_mysql} WHERE" \
                     f" {dish_name_field_mysql}='{dish_name}'"
    return check_existing(checking_query)

def insert_ingredient(name, is_liquid, fat, carbs, fiber, protein,
                      is_vegan, is_vegetarian, is_gluten_free,
                      is_lactose_free, serving):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = insert_ingredient_query(cursor, name, is_liquid, fat, carbs,
                                        fiber, protein, is_vegan, is_vegetarian,
                                        is_gluten_free, is_lactose_free, serving)
    close_connection(conn, cursor)
    return error

def get_dish_info_by_name(dish_name):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_dish_info_query(cursor, dish_name)
    close_connection(conn, cursor)
    return error, found, result

def get_ingredient_info_by_name(ingredient_name):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_ingredient_info_query(cursor, ingredient_name)
    close_connection(conn, cursor)
    return error, found, result

def insert_dish_query(conn, cursor, dish_name, ingredients_amount_dict):
    insertion_arr = []

    query = f"INSERT INTO {dishes_table_mysql} ({dish_name_field_mysql}) VALUES (%s)"
    val = (dish_name, )
    insertion_arr.append((query, val))

    for ingredient in ingredients_amount_dict:
        amount = ingredients_amount_dict[ingredient]
        query = f"INSERT INTO {dish_ingredients_table_mysql} ({dish_name_field_mysql}," \
                f" {ingredient_name_field_mysql}, {ingredient_amount_field_mysql}) VALUES" \
                f" (%s, %s, %s)"
        val = (dish_name, ingredient, amount)
        insertion_arr.append((query, val))

    return mysql_multiple_action(conn, cursor, insertion_arr)

def add_ingredient_amount(ingredients_amount_dict, ingredient, amount):
    curr_amount = 0

    if ingredient in ingredients_amount_dict:
        curr_amount = ingredients_amount_dict[ingredient]
    ingredients_amount_dict[ingredient] = amount + curr_amount

    return ingredients_amount_dict

def get_ingredients_amount_of_dish(cursor, dish_name, percent, ingredients_amount_dict):
    found = False
    query = f"SELECT * FROM {dish_ingredients_table_mysql} WHERE {dish_name_field_mysql}='{dish_name}'"

    error, result = mysql_getting_action(cursor, query, False)
    if not error and result:
        found = True
        for row in result:
            ingredient = row[ingredient_name_field_mysql]
            amount = row[ingredient_amount_field_mysql] * percent
            ingredients_amount_dict = \
                add_ingredient_amount(ingredients_amount_dict, ingredient, amount)

    return error, found, ingredients_amount_dict

def check_dish_params(dish):
    return isinstance(dish, dict) and dish_name_field_param in dish and \
           dish_percent_field_param in dish and len(dish) == 2

def fill_ingredients_dict_by_dishes(cursor, dishes, ingredients_amount_dict):
    error = not isinstance(dishes, list)
    for dish in dishes:
        if error:
            break
        error = True
        found = False
        if check_dish_params(dish):
            error = False
        if not error:
            dish_name = dish[dish_name_field_param]
            percent = dish[dish_percent_field_param]
            error, found, ingredients_amount_dict = \
                get_ingredients_amount_of_dish(cursor, dish_name, percent, ingredients_amount_dict)
        error = error or not found

    return error, ingredients_amount_dict

def check_ingredient_params(ingredient):
    return isinstance(ingredient, dict) and ingredient_name_field_param in ingredient and \
           ingredient_amount_field_param in ingredient and len(ingredient) == 2

def fill_ingredients_dict_by_ingredients(ingredients, ingredients_amount_dict):
    error = not isinstance(ingredients, list)
    for ingredient in ingredients:
        if error:
            break
        error = True
        if check_ingredient_params(ingredient):
            error = False
        if not error:
            ingredient_name = ingredient[ingredient_name_field_param]
            amount = ingredient[ingredient_amount_field_param]
            ingredients_amount_dict = \
                add_ingredient_amount(ingredients_amount_dict, ingredient_name, amount)
    return error, ingredients_amount_dict

def insert_dish(name, ingredients, dishes):
    conn, cursor, error = get_mysql_cursor()
    ingredients_amount_dict = {}

    if not error:
        error, ingredients_amount_dict = \
            fill_ingredients_dict_by_dishes(cursor, dishes, ingredients_amount_dict)
    if not error:
        error, ingredients_amount_dict = \
            fill_ingredients_dict_by_ingredients(ingredients, ingredients_amount_dict)
    if not error:
        error = insert_dish_query(conn, cursor, name, ingredients_amount_dict)

    close_connection(conn, cursor)
    return error