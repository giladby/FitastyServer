from Mysql_Food_Handling import *
from urllib.parse import urlparse, parse_qs
from Server_Utils import *
from Macros import *
from http import HTTPStatus

def server_insert_dish(server):
    return

def check_get_ingredients_params(data):
    error = True
    if data and name_begin_field_param in data and \
            is_vegan_field_param in data and is_vegetarian_field_param in data and \
            is_lactose_free_field_param in data and \
            is_gluten_free_field_param in data and len(data) == 5:
        error = False
    return error

def get_ingredients_by_data(data, include_dish):
    begin_name = data[name_begin_field_param]
    is_vegan = data[is_vegan_field_param]
    is_vegetarian = data[is_vegetarian_field_param]
    is_lactose_free = data[is_lactose_free_field_param]
    is_gluten_free = data[is_gluten_free_field_param]

    return get_filtered_ingredients(begin_name, is_vegan, is_vegetarian,
                                    is_lactose_free, is_gluten_free, include_dish)

def server_get_ingredients(server):
    print("in get_ingredients")
    error = True
    result = None
    data = None
    include_dish = None

    qs = parse_qs(urlparse(server.path).query)
    if include_dish_field_param in qs and len(qs) == 1:
        include_dish = qs[include_dish_field_param][0]
        error = False

    if not error:
        error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_get_ingredients_params(data)

    if not error:
        error, result = get_ingredients_by_data(data, include_dish)

    if not error:
        send_json(server, result)
    else:
        send_error(server,
                   HTTPStatus.NOT_FOUND.value if not error else HTTPStatus.BAD_REQUEST.value)

def check_insert_ingredient_params(data):
    error = True
    if data and name_field_param in data and is_liquid_field_param in data and \
            fat_field_param in data and carbs_field_param in data and \
            fiber_field_param in data and protein_field_param in data and \
            is_vegan_field_param in data and is_vegetarian_field_param in data and \
            is_lactose_free_field_param in data and \
            is_gluten_free_field_param in data and len(data) == 10:
        error = False
    return error

def insert_ingredient_by_data(data):
    name = data[name_field_param]
    is_liquid = data[is_liquid_field_param]
    fat = data[fat_field_param]
    carbs = data[carbs_field_param]
    fiber = data[fiber_field_param]
    protein = data[protein_field_param]
    is_vegan = data[is_vegan_field_param]
    is_vegetarian = data[is_vegetarian_field_param]
    is_lactose_free = data[is_lactose_free_field_param]
    is_gluten_free = data[is_gluten_free_field_param]

    return insert_ingredient(name, is_liquid, fat, carbs, fiber, protein,
                             is_vegan, is_vegetarian, is_lactose_free, is_gluten_free)

def server_insert_ingredient(server):
    print("in insert_ingredient")
    found = False

    error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_insert_ingredient_params(data)

    if not error:
        ingredient_name = data[name_field_param]
        found, error = check_ingredient(ingredient_name)

    if not error and not found:
        error = insert_ingredient_by_data(data)

    if not error:
        send_json(server, {'name_exist': found})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)