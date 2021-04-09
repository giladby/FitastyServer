from Mysql_Diet_Diaries_Handling import *
from urllib.parse import urlparse, parse_qs
from Server_Utils import *
from Macros import *
from http import HTTPStatus
from Utils import *

# ======================================================================================================================
# insert_diet_diary REQUEST

def check_insert_diet_diary_params(data):
    error = True
    if data and diet_diary_name_field_param in data and meals_field_param in data and \
            len(data) == 2:
        error = False
    return error

def insert_diet_diary_by_data(data, username):
    diet_diary_name = data[diet_diary_name_field_param]
    meals = data[meals_field_param]

    return insert_diet_diary(username, diet_diary_name, meals)

def server_insert_diet_diary(server):
    print("in insert_diet_diary")
    found = False
    qs = None
    username = None

    error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_insert_diet_diary_params(data)

    if not error:
        qs = parse_qs(urlparse(server.path).query)
        error = username_field_param not in qs or len(qs) != 1

    if not error:
        username = qs[username_field_param][0]
        diet_diary_name = data[diet_diary_name_field_param]
        found, error = check_diet_diary(diet_diary_name, username)

    if not error and not found:
        error = insert_diet_diary_by_data(data, username)

    if not error:
        send_json(server, {name_exist_field_param: found})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)

# ======================================================================================================================
# get_diet_diary REQUEST

def server_get_diet_diary(server):
    result = None
    found = False
    qs = parse_qs(urlparse(server.path).query)
    error = diet_diary_name_field_param not in qs or username_field_param not in qs or len(qs) != 2

    if not error:
        username = qs[username_field_param][0]
        diet_diary_name = qs[diet_diary_name_field_param][0]
        error, found, result = get_diet_diary(diet_diary_name, username)

    if not error and found:
        send_json(server, result)
    else:
        send_error(server,
                    HTTPStatus.NOT_FOUND.value if not error else HTTPStatus.BAD_REQUEST.value)

# ======================================================================================================================
# get_diet_diary REQUEST

def server_get_diet_diaries(server):
    found = False
    result = None
    qs = parse_qs(urlparse(server.path).query)
    error = username_field_param not in qs or len(qs) != 1

    if not error:
        if not error:
            username = qs[username_field_param][0]
            error, found, result = get_diet_diaries_names(username)

    if not error and found:
        send_json(server, result)
    else:
        send_error(server,
                   HTTPStatus.NOT_FOUND.value if not error else HTTPStatus.BAD_REQUEST.value)