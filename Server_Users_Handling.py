from Mysql_Users_Handling import *
from urllib.parse import urlparse, parse_qs
from Server_Utils import *
from Macros import *
from http import HTTPStatus

def server_check_username(server):
    print("in check_username")
    error = True
    result = None

    qs = parse_qs(urlparse(server.path).query)
    if username_field_param in qs and len(qs) == 1:
        username = qs[username_field_param][0]
        result, error = check_user(username, False, None)
    if not error:
        send_json(server, {name_exist_field_param: result})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)

def server_log_in(server):
    print("in log_in")
    error = True
    result = None

    qs = parse_qs(urlparse(server.path).query)
    if username_field_param in qs and password_field_param in qs and len(qs) == 2:
        username = qs[username_field_param][0]
        password = qs[password_field_param][0]
        result, error = check_user(username, True, password)
    if not error:
        send_json(server, {found_field_param: result})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)

def check_insert_account_params(data):
    error = True
    if data and password_field_param in data and username_field_param in data and \
            age_field_param in data and is_male_field_param in data and \
            height_field_param in data and weight_field_param in data and \
            activity_factor_field_param in data and diet_type_field_param in data and \
            weight_goal_field_param in data and len(data) == 9:
        error = False
    return error

def insert_update_user_by_data(data, insert, prev_username):
    username = data[username_field_param]
    password = data[password_field_param]
    age = data[age_field_param]
    is_male = data[is_male_field_param]
    height = data[height_field_param]
    weight = data[weight_field_param]
    activity_factor = data[activity_factor_field_param]
    diet_type = data[diet_type_field_param]
    weight_goal = data[weight_goal_field_param]

    if insert:
        error = insert_user(username, password, age, is_male, height, weight,
                            activity_factor, diet_type, weight_goal)
    else:
        error = update_user(prev_username, username, password, age, is_male, height,
                            weight, activity_factor, diet_type, weight_goal)

    return error

def server_delete_account(server):
    print("in delete_account")
    found = False
    error = True
    username = None
    code = HTTPStatus.OK

    qs = parse_qs(urlparse(server.path).query)
    if username_field_param in qs and len(qs) == 1:
        error = False

    if not error:
        username = qs[username_field_param][0]
        found, error = check_user(username, False, None)

    if not error and found:
        error = delete_user(username)

    if error:
        code = HTTPStatus.BAD_REQUEST
    elif not found:
        code = HTTPStatus.NOT_FOUND

    send_error(server, code.value)

def server_insert_account(server):
    print("in insert_account")
    found = False

    error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_insert_account_params(data)

    if not error:
        username = data[username_field_param]
        found, error = check_user(username, False, None)

    if not error and not found:
        error = insert_update_user_by_data(data, True, None)

    if not error:
        send_json(server, {name_exist_field_param: found})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)

def server_get_account_info(server):
    print("in get_account_info")
    error = True
    found = False
    result = None

    qs = parse_qs(urlparse(server.path).query)
    if username_field_param in qs and len(qs) == 1:
        username = qs[username_field_param][0]
        error, found, result = get_account_info_by_username(username)

    if not error and found:
        send_json(server, result)
    else:
        send_error(server,
                   HTTPStatus.NOT_FOUND.value if not error else HTTPStatus.BAD_REQUEST.value)

def server_update_account(server):
    error = True
    data = None
    found = False

    qs = parse_qs(urlparse(server.path).query)
    if prev_username_field_param in qs or len(qs) == 1:
        error = False

    if not error:
        error, data = read_json_convert_to_dictionary(server)

    if not error:
        error = check_insert_account_params(data)

    if not error:
        prev_username = qs[prev_username_field_param][0]
        username = data[username_field_param]
        if username != prev_username:
            found, error = check_user(username, False, None)

    if not error and not found:
        prev_username = qs[prev_username_field_param][0]
        error = insert_update_user_by_data(data, False, prev_username)

    if not error:
        send_json(server, {name_exist_field_param: found})
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)

