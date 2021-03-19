from Mysql_Connection_General import *
from Macros import *
from Utils import *

def check_ingredient_query(cursor, ingredient_name):
    found = False
    query = f"SELECT * FROM {food_ingredients_table_mysql} WHERE" \
            f" {name_field_mysql}='{ingredient_name}'"

    error, result = mysql_getting_action(cursor, query, True)
    if result:
        found = True

    return found, error

def insert_ingredient_query(conn, cursor, name, is_liquid, fat, carbs, fiber, protein,
                            is_vegan, is_vegetarian, is_lactose_free, is_gluten_free):
    query = f"INSERT INTO {food_ingredients_table_mysql} ({name_field_mysql}," \
            f" {is_liquid_field_mysql}, {fat_field_mysql}, {carbs_field_mysql}," \
            f" {fiber_field_mysql}, {protein_field_mysql}, {is_vegan_field_mysql}," \
            f" {is_vegetarian_field_mysql}, {is_lactose_free_field_mysql}," \
            f" {is_gluten_free_field_mysql}) VALUES" \
            f" (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, convert_boolean_to_number(is_liquid), fat, carbs, fiber, protein,
           convert_boolean_to_number(is_vegan), convert_boolean_to_number(is_vegetarian),
           convert_boolean_to_number(is_lactose_free), convert_boolean_to_number(is_gluten_free))

    return mysql_insertion_action(conn, cursor, query, val)

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

def get_filtered_ingredients_query(cursor, begin_name, is_vegan, is_vegetarian,
                                   is_lactose_free, is_gluten_free, include_dish):
    if include_dish == include_dish_positive_param_val:
        query = get_ingredients_and_dishes_query_str(begin_name, is_vegan, is_vegetarian,
                                                     is_lactose_free, is_gluten_free)
    else:
        query = get_ingredients_query_str(begin_name, is_vegan, is_vegetarian,
                                          is_lactose_free, is_gluten_free)
    error, result = mysql_getting_action(cursor, query, False)
    if not error:
        result = convert_result_to_boolean(result)
        result = create_dict_result(result)

    return error, result

def get_filtered_ingredients(begin_name, is_vegan, is_vegetarian,
                             is_lactose_free, is_gluten_free, include_dish):
    result = None
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, result = get_filtered_ingredients_query(cursor, begin_name, is_vegan, is_vegetarian,
                                                       is_lactose_free, is_gluten_free, include_dish)
    close_connection(conn, cursor)
    return error, result

def check_ingredient(ingredient_name):
    conn, cursor, error = get_mysql_cursor()
    result = None
    if not error:
        result, error = check_ingredient_query(cursor, ingredient_name)
    close_connection(conn, cursor)
    return result, error

def insert_ingredient(name, is_liquid, fat, carbs, fiber, protein,
                      is_vegan, is_vegetarian, is_lactose_free, is_gluten_free):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = insert_ingredient_query(conn, cursor, name, is_liquid, fat, carbs,
                                        fiber, protein, is_vegan, is_vegetarian,
                                        is_lactose_free, is_gluten_free)
    close_connection(conn, cursor)
    return error