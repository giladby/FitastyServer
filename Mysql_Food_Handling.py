from Mysql_Connection_General import *
from Macros import *
from Utils import *

def make_ingredient_info_dict(mysql_user_record):
    return {f"{name_field_param}": mysql_user_record[name_field_mysql_position],
            f"{is_liquid_field_param}": mysql_user_record[is_liquid_field_mysql_position] == 1,
            f"{fat_field_param}": mysql_user_record[fat_field_mysql_position],
            f"{carb_field_param}": mysql_user_record[carb_field_mysql_position],
            f"{fiber_field_param}": mysql_user_record[fiber_field_mysql_position],
            f"{protein_field_param}": mysql_user_record[protein_field_mysql_position],
            f"{is_vegan_field_param}": mysql_user_record[is_vegan_field_mysql_position] == 1,
            f"{is_vegetarian_field_param}": mysql_user_record[is_vegetarian_field_mysql_position] == 1,
            f"{is_gluten_free_field_param}": mysql_user_record[is_gluten_free_field_mysql_position] == 1,
            f"{is_lactose_free_field_param}": mysql_user_record[is_lactose_free_field_mysql_position] == 1,
            f"{serving_size_field_param}": mysql_user_record[serving_size_field_mysql_position]}

def get_ingredient_info_query(cursor, ingredient_name):
    found = False
    query = f"SELECT * FROM {food_ingredients_table_mysql} WHERE {name_field_mysql}='{ingredient_name}'"

    error, result = mysql_getting_action(cursor, query, True)
    if not error and result:
        found = True
        result = make_ingredient_info_dict(result)

    return error, found, result

def insert_ingredient_query(cursor, name, is_liquid, fat, carbs, fiber, protein,
                            is_vegan, is_vegetarian,is_gluten_free,
                            is_lactose_free, serving):
    query = f"INSERT INTO {food_ingredients_table_mysql} ({name_field_mysql}," \
            f" {is_liquid_field_mysql}, {fat_field_mysql}, {carb_field_mysql}," \
            f" {fiber_field_mysql}, {protein_field_mysql}, {is_vegan_field_mysql}," \
            f" {is_vegetarian_field_mysql}, {is_gluten_free_field_mysql}," \
            f" {is_lactose_free_field_mysql}, {serving_size_field_mysql}) VALUES" \
            f" (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, convert_boolean_to_number(is_liquid), fat, carbs, fiber, protein,
           convert_boolean_to_number(is_vegan), convert_boolean_to_number(is_vegetarian),
           convert_boolean_to_number(is_gluten_free),
           convert_boolean_to_number(is_lactose_free), serving)

    return mysql_insertion_action(cursor, query, val)

def convert_result_to_boolean(result):
    for i in range(len(result)):
        tuple = result[i]
        ingredient_name = tuple[0]
        is_liquid_boolean = True if tuple[1] == 1 else False
        result[i] = {f"{name_field_param}": ingredient_name,
                     f"{is_liquid_field_param}": is_liquid_boolean}
    return result


def create_dict_result(result):
    return {f"{ingredients_field_param}": result}

def get_ingredients_and_dishes_query_str(begin_name, is_vegan, is_vegetarian,
                                         is_lactose_free, is_gluten_free):
    return ""

def get_ingredients_query_str(begin_name, is_vegan, is_vegetarian,
                              is_lactose_free, is_gluten_free):
    query = f"SELECT {name_field_mysql}, {is_liquid_field_mysql} FROM {food_ingredients_table_mysql}" \
            f" WHERE {name_field_mysql} LIKE '{begin_name}%'"
    if is_vegan is not None:
        vegan = 1 if is_vegan else 0
        query += f" AND {is_vegan_field_mysql} = '{vegan}'"
    if is_vegetarian is not None:
        vegetarian = 1 if is_vegetarian else 0
        query += f" AND {is_vegetarian_field_mysql} = '{vegetarian}'"
    if is_lactose_free is not None:
        lactose_free = 1 if is_lactose_free else 0
        query += f" AND {is_lactose_free_field_mysql} = '{lactose_free}'"
    if is_gluten_free is not None:
        gluten_free = 1 if is_gluten_free else 0
        query += f" AND {is_gluten_free_field_mysql} = '{gluten_free}'"

    return query

def get_filtered_foods_query(cursor, begin_name,max_fat, max_carb, max_fiber,
                             max_protein, min_fat, min_carb, min_fiber,
                             min_protein, is_vegan, is_vegetarian,
                             is_lactose_free, is_gluten_free, include_dish, include_ingredient):
    #query = ...
    #error, result = mysql_getting_action(cursor, query, False)
    #if not error:
    #    result = convert_result_to_boolean(result)
    #    result = create_dict_result(result)

    #return error, result
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
                     f" {name_field_mysql}='{ingredient_name}'"
    return check_existing(checking_query)

def check_dish(dish_name):
    checking_query = f"SELECT * FROM {dishes_table_mysql} WHERE" \
                     f" {name_field_mysql}='{dish_name}'"
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

def get_ingredient_info_by_name(ingredient_name):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_ingredient_info_query(cursor, ingredient_name)
    close_connection(conn, cursor)
    return error, found, result

def insert_dish_query(conn, cursor, name, is_liquid, ingredients_arr, dishes_arr):
    query = f"INSERT INTO {food_ingredients_table_mysql} ({name_field_mysql}," \
            f" {is_liquid_field_mysql}, {fat_field_mysql}, {carb_field_mysql}," \
            f" {fiber_field_mysql}, {protein_field_mysql}, {is_vegan_field_mysql}," \
            f" {is_vegetarian_field_mysql}, {is_gluten_free_field_mysql}," \
            f" {is_lactose_free_field_mysql}, {serving_size_field_mysql}) VALUES" \
            f" (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, convert_boolean_to_number(is_liquid), fat, carbs, fiber, protein,
           convert_boolean_to_number(is_vegan), convert_boolean_to_number(is_vegetarian),
           convert_boolean_to_number(is_gluten_free),
           convert_boolean_to_number(is_lactose_free), serving)

    return mysql_insertion_action(conn, cursor, query, val)

def get_ingredients_amount_of_dish(cursor, dish_name, percent, ingredients_amount):
    found = False
    query = f"SELECT * FROM {dish_ingredients_table_mysql} WHERE {dish_name_field_mysql}='{dish_name}'"

    error, result = mysql_getting_action(cursor, query, False)
    if not error and result:
        found = True
        for row in result:
            ingredient = row[ingredient_name_field_mysql_position]
            amount = row[ingredient_amount_field_mysql_position] * percent
            curr_amount = 0
            if ingredient in ingredients_amount:
                curr_amount = ingredients_amount[ingredient]
            ingredients_amount[ingredient] = amount + curr_amount

    return error, found, ingredients_amount

def get_dishes_arr(cursor, dishes, ingredients_amount):
    error = not isinstance(dishes, list)
    if not error:
        for dish in dishes:
            ok_params = isinstance(dish, list) and dish_name_field_param in dish and \
                        dish_percent_field_param in dish and len(dish) == 2
            if not ok_params:
                error = True
                break
            dish_name = dish[dish_name_field_param]
            percent = dish[dish_percent_field_param]
            error, found, ingredients_amount = \
                get_ingredients_amount_of_dish(cursor, dish_name, percent, ingredients_amount)
            error = error or not found
    return error, ingredients_amount

def insert_dish(name, is_liquid, ingredients, dishes):
    conn, cursor, error = get_mysql_cursor()
    dishes_arr = []
    ingredients_arr = []

    if not error:
        error, dishes_arr = get_dishes_arr(dishes)


    if not error:
        error = insert_dish_query(conn, cursor, name, is_liquid, ingredients_arr, dishes_arr)
    close_connection(conn, cursor)
    return error