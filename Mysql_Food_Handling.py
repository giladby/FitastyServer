from Mysql_Connection_General import *
from Macros import *
from Utils import *
import math

# ======================================================================================================================
# get_dish_info QUERY

def make_dish_info_dict(dish_name, mysql_user_records):
    fat = 0
    carb = 0
    fiber = 0
    protein = 0
    ingredients_arr = []

    for record in mysql_user_records:
        mulitplier = record[ingredient_amount_field_mysql] / 100
        fat += record[fat_field_mysql] * mulitplier
        carb += record[carb_field_mysql] * mulitplier
        fiber += record[fiber_field_mysql] * mulitplier
        protein += record[protein_field_mysql] * mulitplier
        ingredient_list = {f"{ingredient_name_field_param}": record[ingredient_name_field_mysql],
                           f"{is_liquid_field_param}": record[is_liquid_field_mysql] == 1,
                           f"{ingredient_amount_field_param}": record[ingredient_amount_field_mysql]}
        ingredients_arr.append(ingredient_list)

    return {f"{dish_name_field_param}": dish_name,
            f"{fat_field_param}": fat,
            f"{carb_field_param}": carb,
            f"{fiber_field_param}": fiber,
            f"{protein_field_param}": protein,
            f"{ingredients_field_param}": ingredients_arr}

def get_dish_info_query(cursor, dish_name):
    found = False
    query = f"SELECT * FROM {dish_ingredients_table_mysql} JOIN {food_ingredients_table_mysql}" \
            f" ON ({dish_ingredients_table_mysql}.{ingredient_name_field_mysql} =" \
            f" {food_ingredients_table_mysql}.{ingredient_name_field_mysql})" \
            f" WHERE {dish_name_field_mysql} = %s"
    val = (dish_name,)
    error, result = mysql_getting_action(cursor, query, val, False)
    if not error and result:
        found = True
        result = make_dish_info_dict(dish_name, result)

    return error, found, result

def get_dish_info_by_name(dish_name):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_dish_info_query(cursor, dish_name)
    close_connection(conn, cursor)
    return error, found, result

# ======================================================================================================================
# get_ingredient_info QUERY

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
    query = f"SELECT * FROM {food_ingredients_table_mysql} WHERE {ingredient_name_field_mysql} = %s"
    val = (ingredient_name,)
    error, result = mysql_getting_action(cursor, query, val, True)
    if not error and result:
        found = True
        result = make_ingredient_info_dict(result)

    return error, found, result

def get_ingredient_info_by_name(ingredient_name):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_ingredient_info_query(cursor, ingredient_name)
    close_connection(conn, cursor)
    return error, found, result

# ======================================================================================================================
# insert_ingredient QUERY

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

# ======================================================================================================================
# get_foods QUERY

def get_min_max_percent(min_input, max_input):
    max_result = max_input if max_input else math.inf
    min_result = min_input if min_input else 0

    return min_result, max_result

def sum_prefix_string():
    return "sum_"

def sum_prefix(element):
    return f"{sum_prefix_string()}{element}"

def sum_element_in_query(element):
    return f"SUM({element}) AS {sum_prefix(element)}"

def convert_amount(to_convert):
    return f"{to_convert}*{ingredient_amount_field_mysql}/100 as {to_convert}"

def get_filtered_dishes_query(cursor, begin_name, fat, carb, fiber,
                              protein, is_vegan, is_vegetarian,
                              is_lactose_free, is_gluten_free, min_percent, max_percent):
    query = f"SELECT {dish_name_field_mysql}," \
            f" {sum_element_in_query(fat_field_mysql)}, {sum_element_in_query(carb_field_mysql)}," \
            f" {sum_element_in_query(fiber_field_mysql)}, {sum_element_in_query(protein_field_mysql)}," \
            f" BIT_AND({is_vegan_field_mysql}) as bit_vegan," \
            f" BIT_AND({is_vegetarian_field_mysql}) as bit_vegetarian," \
            f" BIT_AND({is_gluten_free_field_mysql}) as bit_gluten," \
            f" BIT_AND({is_lactose_free_field_mysql}) as bit_lactose" \
            f" FROM (SELECT {dish_name_field_mysql}, {convert_amount(fat_field_mysql)}," \
                     f" {convert_amount(carb_field_mysql)}, {convert_amount(fiber_field_mysql)}," \
                     f" {convert_amount(protein_field_mysql)}, {is_vegan_field_mysql}, {is_vegetarian_field_mysql}," \
                     f" {is_lactose_free_field_mysql}, {is_gluten_free_field_mysql}" \
                     f" FROM {food_ingredients_table_mysql} JOIN {dish_ingredients_table_mysql}" \
                     f" ON ({food_ingredients_table_mysql}.{ingredient_name_field_mysql} =" \
                     f" {dish_ingredients_table_mysql}.{ingredient_name_field_mysql})) AS joined_table" \
            f" GROUP BY {dish_name_field_mysql}" \
            f" HAVING {dish_name_field_mysql} LIKE %s"
    val = (f"{begin_name}%",)

    check_none_arr = {f"{fat_field_mysql}": fat, f"{carb_field_mysql}": carb,
                      f"{fiber_field_mysql}": fiber, f"{protein_field_mysql}": protein}
    check_boolean_arr = {"bit_vegan": is_vegan, "bit_vegetarian": is_vegetarian,
                         "bit_gluten": is_gluten_free, "bit_lactose": is_lactose_free}

    required_dict = {}
    for check_none in check_none_arr:
        value = check_none_arr[check_none]
        if value is not None:
            query += f" AND {min_percent}*{sum_prefix(check_none)} <= %s"
            val += (value,)
            required_dict[check_none] = value
        if value is not None and max_percent != math.inf:
            query += f" AND %s <= {max_percent}*{sum_prefix(check_none)}"
            val += (value,)

    for check_boolean in check_boolean_arr:
        boolean_value = check_boolean_arr[check_boolean]
        if boolean_value:
            query += f" AND {check_boolean} = 1"

    error, dishes = mysql_getting_action(cursor, query, val, False)

    return error, dishes, required_dict

def add_serving_prefix(string):
    return f"serving_{string}"

def convert_field_by_serving(field):
    return f"{field}/100*serving as {add_serving_prefix(field)}"

def get_filtered_ingredients_query(cursor, begin_name, fat, carb, fiber,
                                   protein, is_vegan, is_vegetarian,
                                   is_lactose_free, is_gluten_free, min_percent, max_percent):

    query = f"SELECT {ingredient_name_field_mysql}, {is_liquid_field_mysql}," \
            f" {fat_field_mysql}, {convert_field_by_serving(fat_field_mysql)}," \
            f" {carb_field_mysql}, {convert_field_by_serving(carb_field_mysql)}," \
            f" {fiber_field_mysql}, {convert_field_by_serving(fiber_field_mysql)}," \
            f" {protein_field_mysql}, {convert_field_by_serving(protein_field_mysql)}" \
            f" FROM {food_ingredients_table_mysql}" \
            f" WHERE {ingredient_name_field_mysql} LIKE %s"
    val = (f"{begin_name}%", )

    check_boolean_arr = {f"{is_vegan_field_mysql}": is_vegan, f"{is_vegetarian_field_mysql}": is_vegetarian,
                         f"{is_gluten_free_field_mysql}": is_gluten_free,
                         f"{is_lactose_free_field_mysql}": is_lactose_free}

    for check_boolean in check_boolean_arr:
        boolean_value = check_boolean_arr[check_boolean]
        if boolean_value:
            query += f" AND {check_boolean} = 1"

    check_none_arr = {f"{fat_field_mysql}": fat, f"{carb_field_mysql}": carb,
                      f"{fiber_field_mysql}": fiber, f"{protein_field_mysql}": protein}
    having_str = "HAVING"

    required_dict = {}
    for check_none in check_none_arr:
        value = check_none_arr[check_none]
        check_with_prefix = add_serving_prefix(check_none)
        if value is not None:
            query += f" {having_str} {check_with_prefix}*{min_percent} <= %s"
            val += (value,)
            having_str = "AND"
            required_dict[check_none] = value
        if value is not None and max_percent != math.inf:
            query += f" AND %s <= {check_with_prefix}*{max_percent}"
            val += (value,)

    error, ingredients = mysql_getting_action(cursor, query, val, False)

    return error, ingredients, required_dict

def get_max_percent_amount(data, field_prefix, factor, required_dict):
    result = math.inf
    for element in required_dict:
        field_name = f"{field_prefix}{element}"
        curr_val = data[field_name]
        required_val = required_dict[element]
        curr_result = math.inf if curr_val == 0 else factor * required_val / curr_val
        result = min(result, curr_result)
    return result

def make_dict_result(dishes, ingredients, required_dict):
    dishes_arr = []
    ingredients_arr = []

    for dish in dishes:
        percent = get_max_percent_amount(dish, sum_prefix_string(), 1, required_dict)
        dishes_arr.append({dish_name_field_param: dish[dish_name_field_mysql],
                           dish_percent_field_param: percent})

    for ingredient in ingredients:
        ingredient_name = ingredient[ingredient_name_field_mysql]
        is_liquid = ingredient[is_liquid_field_mysql] == 1
        amount = get_max_percent_amount(ingredient, "", 100, required_dict)
        ingredients_arr.append({ingredient_name_field_param: ingredient_name,
                                is_liquid_field_param: is_liquid,
                                ingredient_amount_field_param: amount})

    return {dishes_field_param: dishes_arr,
            ingredients_field_param: ingredients_arr}

def get_filtered_foods(begin_name, fat, carb, fiber,
                       protein, is_vegan, is_vegetarian,
                       is_lactose_free, is_gluten_free, include_dish, include_ingredient,
                       min_percent, max_percent):
    dishes = []
    ingredients = []
    result = None
    required_dict = None

    conn, cursor, error = get_mysql_cursor()

    min_percent, max_percent = get_min_max_percent(min_percent, max_percent)

    if not error and include_dish:
        error, dishes, required_dict = get_filtered_dishes_query(cursor, begin_name, fat, carb, fiber,
                                                                 protein, is_vegan, is_vegetarian,
                                                                 is_lactose_free, is_gluten_free,
                                                                 min_percent, max_percent)
    if not error and include_ingredient:
        error, ingredients, required_dict = get_filtered_ingredients_query(cursor, begin_name, fat, carb, fiber,
                                                                           protein, is_vegan, is_vegetarian,
                                                                           is_lactose_free, is_gluten_free,
                                                                           min_percent, max_percent)
    if not error:
        result = make_dict_result(dishes, ingredients, required_dict)

    close_connection(conn, cursor)
    return error, result

# ======================================================================================================================
# check_ingredient QUERY

def check_ingredient(ingredient_name):
    checking_query = f"SELECT * FROM {food_ingredients_table_mysql} WHERE" \
                     f" {ingredient_name_field_mysql} = %s"
    val = (ingredient_name,)
    _, found, error = check_existing(checking_query, val)
    return found, error

# ======================================================================================================================
# check_dish QUERY

def check_dish(dish_name):
    checking_query = f"SELECT * FROM {dishes_table_mysql} WHERE" \
                     f" {dish_name_field_mysql} = %s"
    val = (dish_name,)
    _, found, error = check_existing(checking_query, val)
    return found, error

# ======================================================================================================================
# insert_dish QUERY

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
    query = f"SELECT {ingredient_name_field_mysql}," \
            f"{ingredient_amount_field_mysql} * {percent} as {ingredient_amount_field_mysql}" \
            f" FROM {dish_ingredients_table_mysql} WHERE {dish_name_field_mysql} = %s"
    val = (dish_name,)
    error, result = mysql_getting_action(cursor, query, val, False)
    if not error and result:
        found = True
        for row in result:
            ingredient = row[ingredient_name_field_mysql]
            amount = row[ingredient_amount_field_mysql]
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