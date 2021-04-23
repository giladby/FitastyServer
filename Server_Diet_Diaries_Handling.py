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

def insert_update_diet_diary_by_data(data, user_id, prev_diet_diary_name, insert):
    diet_diary_name = data[diet_diary_name_field_param]
    meals = data[meals_field_param]

    if insert:
        result = insert_diet_diary(user_id, diet_diary_name, meals)
    else:
        result = update_diet_diary(prev_diet_diary_name, user_id, diet_diary_name, meals)

    return result

def server_insert_diet_diary(server):
    print("in insert_diet_diary")
    found = False
    qs = None
    user_id = None

    error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_insert_diet_diary_params(data)

    if not error:
        qs = parse_qs(urlparse(server.path).query)
        error = username_field_param not in qs or len(qs) != 1

    if not error:
        username = qs[username_field_param][0]
        diet_diary_name = data[diet_diary_name_field_param]
        user_id, found, error = check_diet_diary(diet_diary_name, username)

    if not error and not found:
        error = insert_update_diet_diary_by_data(data, user_id, None, True)

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
# get_diet_diaries REQUEST

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


# ======================================================================================================================
# delete_diet_diary REQUEST

def server_delete_diet_diary(server):
    print("in delete_diet_diary")
    found = False
    user_id = None
    diet_diary_name= None
    error = True
    code = HTTPStatus.OK

    qs = parse_qs(urlparse(server.path).query)
    if username_field_param in qs and diet_diary_name_field_param in qs and len(qs) == 2:
        error = False

    if not error:
        username = qs[username_field_param][0]
        diet_diary_name = qs[diet_diary_name_field_param][0]
        user_id, found, error = check_diet_diary(diet_diary_name, username)

    if not error and found:
        error = delete_diet_diary(diet_diary_name, user_id)

    if error:
        code = HTTPStatus.BAD_REQUEST
    elif not found:
        code = HTTPStatus.NOT_FOUND

    send_error(server, code.value)


# ======================================================================================================================
# update_diet_diary REQUEST

def server_update_diet_diary(server):
    error = True
    data = None
    found = False
    user_id = None
    prev_diet_diary_name = None

    qs = parse_qs(urlparse(server.path).query)
    if username_field_param in qs and prev_diet_diary_name_field_param in qs or len(qs) == 2:
        error = False

    if not error:
        error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_insert_diet_diary_params(data)

    if not error:
        diet_diary_name = data[diet_diary_name_field_param]
        prev_diet_diary_name = qs[prev_diet_diary_name_field_param][0]
        username = qs[username_field_param][0]
        if diet_diary_name != prev_diet_diary_name:
            user_id, found, error = check_diet_diary(diet_diary_name, username)

    if not error and not found:
        error = insert_update_diet_diary_by_data(data, user_id, prev_diet_diary_name, False)

    if not error:
        send_json(server, {name_exist_field_param: found})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)




