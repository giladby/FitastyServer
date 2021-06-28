from ML_Model import get_probabilities
from Machine_Learning import add_new_ingredient_column, get_featured_row
from Mysql_Connection_General import *
from Macros import *
from Utils import *
from Main import samples_mutex
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
    query = f"SELECT * FROM {dish_ingredients_table_mysql} JOIN {dishes_table_mysql}" \
            f" ON {dish_ingredients_table_mysql}.{dish_id_field_mysql} = {dishes_table_mysql}.{id_field_mysql}" \
            f" JOIN {food_ingredients_table_mysql}" \
            f" ON {dish_ingredients_table_mysql}.{ingredient_id_field_mysql} =" \
            f" {food_ingredients_table_mysql}.{id_field_mysql}" \
            f" WHERE {dishes_table_mysql}.{dish_name_field_mysql} = %s"
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

def insert_ingredient_transaction_main_func(cursor, name, is_liquid, fat, carbs, fiber, protein,
                                            is_vegan, is_vegetarian, is_gluten_free, is_lactose_free, serving):
    error = False
    ingredient_id = None

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

    try:
        cursor.execute(query, val)
        ingredient_id = cursor.lastrowid
    except:
        error = True

    return error, ingredient_id

def insert_ingredient_transaction_func(cursor, args):
    name = args[0]
    is_liquid = args[1]
    fat = args[2]
    carbs = args[3]
    fiber = args[4]
    protein = args[5]
    is_vegan = args[6]
    is_vegetarian = args[7]
    is_gluten_free = args[8]
    is_lactose_free = args[9]
    serving = args[10]

    error, ingredient_id = insert_ingredient_transaction_main_func(cursor, name, is_liquid, fat, carbs, fiber, protein,
                                                                   is_vegan, is_vegetarian, is_gluten_free,
                                                                   is_lactose_free, serving)

    if error:
        raise ValueError()

    with samples_mutex:
        if add_new_ingredient_column(ingredient_id):
            raise ValueError()


def insert_ingredient_query(conn, cursor, name, is_liquid, fat, carbs, fiber, protein, is_vegan,
                            is_vegetarian, is_gluten_free, is_lactose_free, serving):
    return transaction_execute(conn, cursor, insert_ingredient_transaction_func,
                               (name, is_liquid, fat, carbs, fiber, protein, is_vegan, is_vegetarian,
                                is_gluten_free, is_lactose_free, serving))


def insert_ingredient(name, is_liquid, fat, carbs, fiber, protein, is_vegan,
                      is_vegetarian, is_gluten_free, is_lactose_free, serving):
    conn, cursor, error = get_mysql_cursor()

    if not error:
        error = insert_ingredient_query(conn, cursor, name, is_liquid, fat, carbs,
                                        fiber, protein, is_vegan, is_vegetarian,
                                        is_gluten_free, is_lactose_free, serving)

    close_connection(conn, cursor)
    return error

# ======================================================================================================================
# get_foods QUERY

def get_min_max_percent(min_input, max_input):
    max_result = max_input if max_input is not None else math.inf
    min_result = min_input if min_input is not None else 0

    return min_result, max_result

def sum_prefix_string():
    return "sum_"

def sum_prefix(element):
    return f"{sum_prefix_string()}{element}"

def sum_element_in_query(element):
    return f"SUM({element}) AS {sum_prefix(element)}"

def convert_amount(to_convert):
    return f"{to_convert}*{ingredient_amount_field_mysql}/100 as {to_convert}"

def handle_dish_record(dish_record, dishes_dict):
    ingredients_dict = {}
    dish_info = (0, 0, 0, 0, 0, 1, 1, 1, 1)
    dish_name = dish_record[dish_name_field_mysql]
    ingredient = dish_record[ingredient_id_field_mysql]
    amount = dish_record[ingredient_amount_field_mysql]
    fat = dish_record[fat_field_mysql]
    carb = dish_record[carb_field_mysql]
    protein = dish_record[protein_field_mysql]
    fiber = dish_record[fiber_field_mysql]
    is_vegetarian = dish_record[is_vegetarian_field_mysql]
    is_vegan = dish_record[is_vegan_field_mysql]
    is_lactose_free = dish_record[is_lactose_free_field_mysql]
    is_gluten_free = dish_record[is_gluten_free_field_mysql]
    if dish_name in dishes_dict:
        dish_info, ingredients_dict = dishes_dict[dish_name]
    ingredients_dict[ingredient] = amount
    total_amount, dish_fat, dish_carb, dish_protein, dish_fiber, is_dish_vegetarian, is_dish_vegan, \
        is_dish_lactose_free, is_dish_gluten_free = dish_info
    dish_info = (total_amount + amount, dish_fat + fat, dish_carb + carb, dish_fiber + fiber, dish_protein + protein,
                 is_dish_vegetarian and is_vegetarian, is_dish_vegan and is_vegan,
                 is_dish_lactose_free and is_lactose_free, is_dish_gluten_free and is_gluten_free)
    dishes_dict[dish_name] = (dish_info, ingredients_dict)

def create_required_dict(fat, carb, fiber, protein):
    required_dict = {}
    check_arr = {f"{fat_field_mysql}": fat, f"{carb_field_mysql}": carb,
                 f"{fiber_field_mysql}": fiber, f"{protein_field_mysql}": protein}

    for element in check_arr:
        value = check_arr[element]
        if value is not None:
            required_dict[element] = value

    return required_dict

def get_index_by_required_element(required_element):
    index_dict = {f"{fat_field_mysql}": 1, f"{carb_field_mysql}": 2,
                  f"{fiber_field_mysql}": 3, f"{protein_field_mysql}": 4,
                  f"{is_vegetarian_field_mysql}": 5, f"{is_vegan_field_mysql}": 6,
                  f"{is_lactose_free_field_mysql}": 7, f"{is_gluten_free_field_mysql}": 8 }

    return index_dict.get(required_element, -1)

def has_to_be_filtered(dish_info, required_dict, is_vegan, is_vegetarian,
                       is_lactose_free, is_gluten_free, min_percent, max_percent):
    check_boolean_arr = {f"{is_vegan_field_mysql}": is_vegan, f"{is_vegetarian_field_mysql}": is_vegetarian,
                         f"{is_gluten_free_field_mysql}": is_gluten_free,
                         f"{is_lactose_free_field_mysql}": is_lactose_free}
    stay = True

    for element in required_dict:
        if not stay:
            break
        value = required_dict[element]
        dish_val = dish_info[get_index_by_required_element(element)]
        stay = stay and min_percent*dish_val <= value
        stay = stay and max_percent*dish_val >= value if max_percent != math.inf else stay

    for check_boolean in check_boolean_arr:
        if not stay:
            break
        stay = stay and dish_info[get_index_by_required_element(check_boolean)] if check_boolean_arr[check_boolean] \
                else stay

    return not stay

def filter_and_update_dishes(dishes_dict, is_vegan, is_vegetarian, is_lactose_free, is_gluten_free,
                             min_percent, max_percent, required_dict, proba_dict):
    dishes_copy = dishes_dict.copy()
    for dish_name, dish_data in dishes_copy.items():
        dish_info, ingredients_dict = dish_data
        if has_to_be_filtered(dish_info, required_dict, is_vegan, is_vegetarian,
                              is_lactose_free, is_gluten_free, min_percent, max_percent):
            del dishes_dict[dish_name]
        else:
            calculated_val = 0
            total_dish_amount = dish_info[0]
            for ingredient in ingredients_dict:
                ingredient_precent = ingredients_dict[ingredient] / total_dish_amount
                calculated_val += ingredient_precent * proba_dict[ingredient] if ingredient in proba_dict else 0
            dishes_dict[dish_name] = (dish_info, calculated_val)

def get_filtered_dishes_query(cursor, begin_name, fat, carb, fiber, protein, is_vegan, is_vegetarian,
                              is_lactose_free, is_gluten_free, min_percent, max_percent, proba_dict):
    dishes_dict = {}
    required_dict = {}

    query = f"SELECT {dish_name_field_mysql}, {ingredient_id_field_mysql}, {ingredient_amount_field_mysql}," \
            f" {convert_amount(fat_field_mysql)}, {convert_amount(carb_field_mysql)}," \
            f" {convert_amount(fiber_field_mysql)}, {convert_amount(protein_field_mysql)}, {is_vegan_field_mysql}," \
            f" {is_vegetarian_field_mysql}, {is_lactose_free_field_mysql}, {is_gluten_free_field_mysql}" \
            f" FROM {food_ingredients_table_mysql} JOIN {dish_ingredients_table_mysql}" \
            f" ON {food_ingredients_table_mysql}.{id_field_mysql} =" \
            f" {dish_ingredients_table_mysql}.{ingredient_id_field_mysql}" \
            f" JOIN {dishes_table_mysql} ON {dishes_table_mysql}.{id_field_mysql} =" \
            f" {dish_ingredients_table_mysql}.{dish_id_field_mysql}" \
            f" WHERE {dish_name_field_mysql} LIKE %s"
    val = (f"{begin_name}%",)

    error, dishes = mysql_getting_action(cursor, query, val, False)

    if not error:
        required_dict = create_required_dict(fat, carb, fiber, protein)

    if not error and dishes:
        for dish in dishes:
            handle_dish_record(dish, dishes_dict)
        filter_and_update_dishes(dishes_dict, is_vegan, is_vegetarian, is_lactose_free, is_gluten_free,
                                 min_percent, max_percent, required_dict, proba_dict)
        dishes_dict = sorted(dishes_dict.items(), key=lambda dish_elem: dish_elem[1][1], reverse=True)

    return error, dishes_dict, required_dict

def add_serving_prefix(string):
    return f"serving_{string}"

def convert_field_by_serving(field):
    return f"{field}/100*serving as {add_serving_prefix(field)}"

def calc_ingredient_elem_key(element):
    ingredient_info, proba_dict = element
    id = ingredient_info[id_field_mysql]
    result = proba_dict[id] if id in proba_dict else 0
    return result

def get_filtered_ingredients_query(cursor, begin_name, fat, carb, fiber,
                                   protein, is_vegan, is_vegetarian,
                                   is_lactose_free, is_gluten_free, min_percent, max_percent, proba_dict):
    ingredients_union = []
    query = f"SELECT {id_field_mysql}, {ingredient_name_field_mysql}, {is_liquid_field_mysql}," \
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

    if not error:
        for ingredient in ingredients:
            ingredients_union.append((ingredient, proba_dict))
        ingredients_union = sorted(ingredients_union,
                                   key=lambda ingredient_elem: calc_ingredient_elem_key(ingredient_elem), reverse=True)
    return error, ingredients_union, required_dict

def get_ingredient_val_by_element(data, required_elem):
    return data[required_elem]

def get_dish_val_by_element(data, required_elem):
    return data[get_index_by_required_element(required_elem)]

def get_max_percent_amount(data, get_val_by_element, factor, required_dict):
    result = math.inf
    for element in required_dict:
        curr_val = get_val_by_element(data, element)
        required_val = required_dict[element]
        curr_result = math.inf if curr_val == 0 else factor * required_val / curr_val
        result = min(result, curr_result)
    return result

def make_dict_result(dishes, ingredients, required_dict):
    dishes_arr = []
    ingredients_arr = []

    for dish_element in dishes:
        dish_name, dish_info = dish_element
        percent = get_max_percent_amount(dish_info[0], get_dish_val_by_element, 1, required_dict)
        dishes_arr.append({dish_name_field_param: dish_name,
                           dish_percent_field_param: percent})

    for ingredient_element in ingredients:
        ingredient, _ = ingredient_element
        ingredient_name = ingredient[ingredient_name_field_mysql]
        is_liquid = ingredient[is_liquid_field_mysql] == 1
        amount = get_max_percent_amount(ingredient, get_ingredient_val_by_element, 100, required_dict)
        ingredients_arr.append({ingredient_name_field_param: ingredient_name,
                                is_liquid_field_param: is_liquid,
                                ingredient_amount_field_param: amount})

    return {dishes_field_param: dishes_arr,
            ingredients_field_param: ingredients_arr}

def get_filtered_foods(begin_name, fat, carb, fiber,
                       protein, is_vegan, is_vegetarian,
                       is_lactose_free, is_gluten_free, include_dish, include_ingredient,
                       min_percent, max_percent, user_id):
    dishes = []
    ingredients_union = []
    result = None
    required_dict = None
    featured_row = None
    proba_dict = None

    conn, cursor, error = get_mysql_cursor()

    min_percent, max_percent = get_min_max_percent(min_percent, max_percent)
    if not error:
        error, featured_row = get_featured_row(cursor, user_id)
    # get model and predict featured_row using mutex
    if not error:
        error, proba_dict = get_probabilities(featured_row)
    if not error and include_dish:
        error, dishes, required_dict = get_filtered_dishes_query(cursor, begin_name, fat, carb, fiber,
                                                                 protein, is_vegan, is_vegetarian,
                                                                 is_lactose_free, is_gluten_free,
                                                                 min_percent, max_percent, proba_dict)
    if not error and include_ingredient:
        error, ingredients_union, required_dict = get_filtered_ingredients_query(cursor, begin_name, fat, carb, fiber,
                                                                                 protein, is_vegan, is_vegetarian,
                                                                                 is_lactose_free, is_gluten_free,
                                                                                 min_percent, max_percent, proba_dict)
    if not error:
        result = make_dict_result(dishes, ingredients_union, required_dict)

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

def insert_main_dish_query(cursor, dish_name):
    query = f"INSERT INTO {dishes_table_mysql} ({dish_name_field_mysql}) VALUES (%s)"
    val = (dish_name,)
    cursor.execute(query, val)

    return cursor.lastrowid

def insert_dish_ingredient_query(cursor, dish_id, ingredient, ingredients_amount):
    query = f"INSERT INTO {dish_ingredients_table_mysql}" \
            f" ({dish_id_field_mysql}, {ingredient_id_field_mysql}, {ingredient_amount_field_mysql})" \
            f" SELECT %s,{food_ingredients_table_mysql}.{id_field_mysql}, %s" \
            f" FROM {food_ingredients_table_mysql}" \
            f" WHERE {food_ingredients_table_mysql}.{ingredient_name_field_mysql} = %s"
    val = (dish_id, ingredients_amount, ingredient)
    cursor.execute(query, val)

def insert_dish_transaction_func(cursor, args):
    dish_name = args[0]
    ingredients_amount_dict = args[1]

    dish_id = insert_main_dish_query(cursor, dish_name)
    for ingredient in ingredients_amount_dict:
        amount = ingredients_amount_dict[ingredient]
        insert_dish_ingredient_query(cursor, dish_id, ingredient, amount)

def insert_dish_query(conn, cursor, name, ingredients_amount_dict):
    return transaction_execute(conn, cursor, insert_dish_transaction_func,
                               (name, ingredients_amount_dict))

def add_ingredient_amount(ingredients_amount_dict, ingredient, amount):
    curr_amount = 0

    if ingredient in ingredients_amount_dict:
        curr_amount = ingredients_amount_dict[ingredient]
    ingredients_amount_dict[ingredient] = amount + curr_amount

    return ingredients_amount_dict

def get_ingredients_amount_of_dishes(cursor, dishes_percents, dishes_tuple, ingredients_amount_dict):
    dishes_dict_cpy = dishes_percents.copy()
    query = f"SELECT {dish_name_field_mysql}, {ingredient_name_field_mysql}, {ingredient_amount_field_mysql}" \
            f" FROM {dish_ingredients_table_mysql} JOIN {food_ingredients_table_mysql}" \
            f" ON {dish_ingredients_table_mysql}.{ingredient_id_field_mysql} =" \
            f" {food_ingredients_table_mysql}.{id_field_mysql}" \
            f" JOIN {dishes_table_mysql}" \
            f" ON {dish_ingredients_table_mysql}.{dish_id_field_mysql} =" \
            f" {dishes_table_mysql}.{id_field_mysql}" \
            f" WHERE {dish_name_field_mysql} IN({get_prepared_string(len(dishes_tuple))})"
    val = dishes_tuple
    error, result = mysql_getting_action(cursor, query, val, False)

    if not error and result:
        for row in result:
            dish_name = row[dish_name_field_mysql]
            ingredient = row[ingredient_name_field_mysql]
            amount = row[ingredient_amount_field_mysql] * dishes_percents[dish_name]
            if dish_name in dishes_dict_cpy:
                dishes_dict_cpy.pop(dish_name)
            ingredients_amount_dict = \
                add_ingredient_amount(ingredients_amount_dict, ingredient, amount)

    error = error or len(dishes_dict_cpy) > 0

    return error, ingredients_amount_dict

def check_dish_params(dish):
    return isinstance(dish, dict) and dish_name_field_param in dish and \
           dish_percent_field_param in dish and len(dish) == 2

def fill_ingredients_dict_by_dishes(cursor, dishes, ingredients_amount_dict):
    error = not isinstance(dishes, list)
    dishes_percents = {}
    dishes_tuple = None
    for dish in dishes:
        if error:
            break
        error = not check_dish_params(dish)
        if not error:
            dish_name = dish[dish_name_field_param]
            percent = dish[dish_percent_field_param]
            dishes_percents[dish_name] = percent
            dishes_tuple = dishes_tuple + (dish_name,) if dishes_tuple else (dish_name,)
    if not error and len(dishes) > 0:
        error, ingredients_amount_dict = get_ingredients_amount_of_dishes(cursor, dishes_percents, dishes_tuple,
                                                                          ingredients_amount_dict)

    return error, ingredients_amount_dict

def check_ingredient_params(ingredient):
    return isinstance(ingredient, dict) and ingredient_name_field_param in ingredient and \
           ingredient_amount_field_param in ingredient and len(ingredient) == 2

def fill_ingredients_dict_by_ingredients(ingredients, ingredients_amount_dict):
    error = not isinstance(ingredients, list)
    for ingredient in ingredients:
        if error:
            break
        error = not check_ingredient_params(ingredient)
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