from Server_Utils import *
from Macros import *
from http import HTTPStatus

def server_json_echo(server):

    error, data = read_json_convert_to_dictionary(server)

    if not error:
        result = {}

        for key in data:
            result[key] = data[key]

        send_json(server, result)
    else:
        send_error(server, HTTPStatus.BAD_REQUEST.value)