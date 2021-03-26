from Mysql_Food_Handling import *
from urllib.parse import urlparse, parse_qs
from Server_Utils import *
from Macros import *
from http import HTTPStatus

def check_insert_dish_params(data):
    error = True
    if data and dish_name_field_param in data and ingredients_field_param in data and \
            dishes_field_param in data and len(data) == 3:
        error = False
    return error

def insert_dish_by_data(data):
    name = data[dish_name_field_param]
    ingredients = data[ingredients_field_param]
    dishes = data[dishes_field_param]

    return insert_dish(name, ingredients, dishes)

def server_insert_dish(server):
    print("in insert_dish")
    found = False

    error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_insert_dish_params(data)

    if not error:
        dish_name = data[dish_name_field_param]
        found, error = check_dish(dish_name)

    if not error and not found:
        error = insert_dish_by_data(data)

    if not error:
        send_json(server, {name_exist_field_param: found})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)

def check_get_foods_params(data):
    error = True
    if data and name_begin_field_param in data and \
            max_fat_field_param in data and max_carb_field_param in data and \
            max_fiber_field_param in data and max_protein_field_param in data and \
            min_fat_field_param in data and min_carb_field_param in data and \
            min_fiber_field_param in data and min_protein_field_param in data and \
            is_vegan_field_param in data and is_vegetarian_field_param in data and \
            is_lactose_free_field_param in data and \
            is_gluten_free_field_param in data and len(data) == 13:
        error = False
    return error

def get_ingredients_by_data(data, include_dish, include_ingredient):
    begin_name = data[name_begin_field_param]
    max_fat = data[max_fat_field_param]
    max_carb = data[max_carb_field_param]
    max_fiber = data[max_fiber_field_param]
    max_protein = data[max_protein_field_param]
    min_fat = data[min_fat_field_param]
    min_carb = data[min_carb_field_param]
    min_fiber = data[min_fiber_field_param]
    min_protein = data[min_protein_field_param]
    is_vegan = data[is_vegan_field_param]
    is_vegetarian = data[is_vegetarian_field_param]
    is_lactose_free = data[is_lactose_free_field_param]
    is_gluten_free = data[is_gluten_free_field_param]

    return get_filtered_foods(begin_name,max_fat, max_carb, max_fiber,
                              max_protein, min_fat, min_carb, min_fiber,
                              min_protein, is_vegan, is_vegetarian,
                              is_lactose_free, is_gluten_free, include_dish, include_ingredient)

def server_get_foods(server):
    print("in get_foods")
    error = True
    result = None
    data = None
    include_dish = False
    include_ingredient = False

    qs = parse_qs(urlparse(server.path).query)
    if include_dish_field_param in qs and include_ingredient_field_param in qs and len(qs) == 2:
        include_dish = qs[include_dish_field_param][0]
        include_ingredient = qs[include_ingredient_field_param][0]
        error = False

    if not error:
        error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_get_foods_params(data)

    if not error:
        error, result = get_ingredients_by_data(data, include_dish, include_ingredient)

    if not error:
        send_json(server, result)
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)

def check_insert_ingredient_params(data):
    error = True
    if data and ingredient_name_field_param in data and is_liquid_field_param in data and \
            fat_field_param in data and carb_field_param in data and \
            fiber_field_param in data and protein_field_param in data and \
            is_vegan_field_param in data and is_vegetarian_field_param in data and \
            is_gluten_free_field_param in data and \
            is_lactose_free_field_param in data and serving_size_field_param in data and \
            len(data) == 11:
        error = False
    return error

def insert_ingredient_by_data(data):
    name = data[ingredient_name_field_param]
    is_liquid = data[is_liquid_field_param]
    fat = data[fat_field_param]
    carb = data[carb_field_param]
    fiber = data[fiber_field_param]
    protein = data[protein_field_param]
    is_vegan = data[is_vegan_field_param]
    is_vegetarian = data[is_vegetarian_field_param]
    is_gluten_free = data[is_gluten_free_field_param]
    is_lactose_free = data[is_lactose_free_field_param]
    serving = data[serving_size_field_param]

    return insert_ingredient(name, is_liquid, fat, carb, fiber, protein,
                             is_vegan, is_vegetarian, is_gluten_free,
                             is_lactose_free, serving)

def server_insert_ingredient(server):
    print("in insert_ingredient")
    found = False

    error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_insert_ingredient_params(data)

    if not error:
        ingredient_name = data[ingredient_name_field_param]
        found, error = check_ingredient(ingredient_name)

    if not error and not found:
        error = insert_ingredient_by_data(data)

    if not error:
        send_json(server, {name_exist_field_param: found})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)

def server_get_dish_info(server):
    print("in get_dish_info")
    error = True
    found = False
    result = None

    qs = parse_qs(urlparse(server.path).query)
    if dish_name_field_param in qs and len(qs) == 1:
        error = False

    if not error:
        dish_name = qs[dish_name_field_param][0]
        error, found, result = get_dish_info_by_name(dish_name)

    if not error and found:
        send_json(server, result)
    else:
        send_error(server,
                   HTTPStatus.NOT_FOUND.value if not error else HTTPStatus.BAD_REQUEST.value)

def server_get_ingredient_info(server):
    print("in get_ingredient_info")
    error = True
    found = False
    result = None

    qs = parse_qs(urlparse(server.path).query)
    if ingredient_name_field_param in qs and len(qs) == 1:
        error = False

    if not error:
        ingredient_name = qs[ingredient_name_field_param][0]
        error, found, result = get_ingredient_info_by_name(ingredient_name)

    if not error and found:
        send_json(server, result)
    else:
        send_error(server,
                   HTTPStatus.NOT_FOUND.value if not error else HTTPStatus.BAD_REQUEST.value)
