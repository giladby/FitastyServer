from Mysql_Connection_General import *
from Macros import *
from Utils import *

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

def get_filtered_dishes_query(cursor, begin_name, max_fat, max_carb, max_fiber,
                              max_protein, min_fat, min_carb, min_fiber,
                              min_protein, is_vegan, is_vegetarian,
                              is_lactose_free, is_gluten_free):
    query = f"SELECT {dish_name_field_mysql}, SUM({fat_field_mysql}) as sum_fat," \
            f" SUM({carb_field_mysql}) as sum_carb," \
            f" SUM({fiber_field_mysql}) as sum_fiber, SUM({protein_field_mysql}) as sum_protein," \
            f" BIT_AND({is_vegan_field_mysql}) as bit_vegan," \
            f" BIT_AND({is_vegetarian_field_mysql}) as bit_vegetarian," \
            f" BIT_AND({is_gluten_free_field_mysql}) as bit_gluten," \
            f" BIT_AND({is_lactose_free_field_mysql}) as bit_lactose" \
            f" FROM (SELECT {dish_name_field_mysql}, {fat_field_mysql}, {carb_field_mysql}, {fiber_field_mysql}," \
                     f" {protein_field_mysql}, {is_vegan_field_mysql}, {is_vegetarian_field_mysql}," \
                     f" {is_lactose_free_field_mysql}, {is_gluten_free_field_mysql}" \
                     f" FROM {food_ingredients_table_mysql} JOIN {dish_ingredients_table_mysql}" \
                     f" ON ({food_ingredients_table_mysql}.{ingredient_name_field_mysql} =" \
                     f" {dish_ingredients_table_mysql}.{ingredient_name_field_mysql})) as joined_table" \
            f" GROUP BY {dish_name_field_mysql}" \
            f" HAVING {dish_name_field_mysql} LIKE %s"
    val = (f"{begin_name}%",)
    check_none_arr = {"sum_fat": (max_fat, min_fat), "sum_carb": (max_carb, min_carb),
                      "sum_fiber": (max_fiber, min_fiber), "sum_protein": (max_protein, min_protein)}
    check_boolean_arr = {"bit_vegan": is_vegan, "bit_vegetarian": is_vegetarian,
                         "bit_gluten": is_gluten_free, "bit_lactose": is_lactose_free}

    for check_none in check_none_arr:
        value_max = check_none_arr[check_none][0]
        value_min = check_none_arr[check_none][1]
        if value_max is not None:
            query += f" AND {check_none} <= %s"
            val += (value_max,)
        if value_min is not None:
            query += f" AND {check_none} >= %s"
            val += (value_min,)

    for check_boolean in check_boolean_arr:
        boolean_value = check_boolean_arr[check_boolean]
        if boolean_value:
            query += f" AND {check_boolean} = 1"

    error, dishes = mysql_getting_action(cursor, query, val, False)

    return error, dishes

def add_serving_prefix(string):
    return f"serving_{string}"

def convert_field_by_serving(field):
    return f"{field}/100*serving as {add_serving_prefix(field)}"

def get_filtered_ingredients_query(cursor, begin_name, max_fat, max_carb, max_fiber,
                                   max_protein, min_fat, min_carb, min_fiber,
                                   min_protein, is_vegan, is_vegetarian,
                                   is_lactose_free, is_gluten_free):

    query = f"SELECT {ingredient_name_field_mysql}, {is_liquid_field_mysql}," \
            f" {convert_field_by_serving(fat_field_mysql)}," \
            f" {convert_field_by_serving(carb_field_mysql)}, {convert_field_by_serving(fiber_field_mysql)}," \
            f" {convert_field_by_serving(protein_field_mysql)} FROM {food_ingredients_table_mysql}" \
            f" WHERE {ingredient_name_field_mysql} LIKE %s"
    val = (f"{begin_name}%", )

    check_boolean_arr = {f"{is_vegan_field_mysql}": is_vegan, f"{is_vegetarian_field_mysql}": is_vegetarian,
                         f"{is_gluten_free_field_mysql}": is_gluten_free,
                         f"{is_lactose_free_field_mysql}": is_lactose_free}

    for check_boolean in check_boolean_arr:
        boolean_value = check_boolean_arr[check_boolean]
        if boolean_value:
            query += f" AND {check_boolean} = 1"

    check_none_arr = {f"{fat_field_mysql}": (max_fat, min_fat), f"{carb_field_mysql}": (max_carb, min_carb),
                      f"{fiber_field_mysql}": (max_fiber, min_fiber),
                      f"{protein_field_mysql}": (max_protein, min_protein)}
    having_str = "HAVING"

    for check_none in check_none_arr:
        value_max = check_none_arr[check_none][0]
        value_min = check_none_arr[check_none][1]
        check_with_prefix = add_serving_prefix(check_none)
        if value_max is not None:
            query += f" {having_str} {check_with_prefix} <= %s"
            val += (value_max,)
            having_str = "AND"
        if value_min is not None:
            query += f" {having_str} {check_with_prefix} >= %s"
            val += (value_min,)
            having_str = "AND"

    error, ingredients = mysql_getting_action(cursor, query, val, False)

    return error, ingredients

def make_dict_result(dishes, ingredients):
    dishes_arr = []
    ingredients_arr = []

    for dish in dishes:
        dishes_arr.append({dish_name_field_param: dish[dish_name_field_mysql]})

    for ingredient in ingredients:
        ingredient_name = ingredient[ingredient_name_field_mysql]
        is_liquid = ingredient[is_liquid_field_mysql] == 1
        ingredients_arr.append({ingredient_name_field_param: ingredient_name,
                                is_liquid_field_param: is_liquid})

    return {dishes_field_param: dishes_arr,
            ingredients_field_param: ingredients_arr}

def get_filtered_foods(begin_name, max_fat, max_carb, max_fiber,
                       max_protein, min_fat, min_carb, min_fiber,
                       min_protein, is_vegan, is_vegetarian,
                       is_lactose_free, is_gluten_free, include_dish, include_ingredient):
    dishes = []
    ingredients = []
    result = None

    conn, cursor, error = get_mysql_cursor()

    if not error and include_dish:
        error, dishes = get_filtered_dishes_query(cursor, begin_name,max_fat, max_carb, max_fiber,
                                                  max_protein, min_fat, min_carb, min_fiber,
                                                  min_protein, is_vegan, is_vegetarian,
                                                  is_lactose_free, is_gluten_free)
    if not error and include_ingredient:
        error, ingredients = get_filtered_ingredients_query(cursor, begin_name,max_fat, max_carb, max_fiber,
                                                       max_protein, min_fat, min_carb, min_fiber,
                                                       min_protein, is_vegan, is_vegetarian,
                                                       is_lactose_free, is_gluten_free)
    if not error:
        result = make_dict_result(dishes, ingredients)

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