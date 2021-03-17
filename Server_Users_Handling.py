from Mysql_Users_Handling import *
from urllib.parse import urlparse, parse_qs
import json
import cgi
from http import HTTPStatus

username_field_json = 'username'
password_field_json = 'password'


def server_check_username(self):
    print("in check_username")
    error = True
    result = None

    qs = parse_qs(urlparse(self.path).query)
    if username_field_json in qs and len(qs) == 1:
        username = qs[username_field_json][0]
        result, error = check_user(username, False, None)
    if not error:
        self._set_headers()
        json_string = json.dumps({'username_exist': result})
        self.wfile.write(json_string.encode(encoding='utf_8'))
    else:
        self.send_response(HTTPStatus.BAD_REQUEST.value)
        self.end_headers()


def server_log_in(server):
    print("in log_in")
    error = True
    result = None

    qs = parse_qs(urlparse(server.path).query)
    if username_field_json in qs and password_field_json in qs and len(qs) == 2:
        username = qs[username_field_json][0]
        password = qs[password_field_json][0]
        result, error = check_user(username, True, password)
    if not error:
        server._set_headers()
        json_string = json.dumps({'found': result})
        server.wfile.write(json_string.encode(encoding='utf_8'))
    else:
        server.send_response(HTTPStatus.BAD_REQUEST.value)
        server.end_headers()


def server_insert_account(server):
    print("in insert_account")
    error = True
    content = server.headers.get('content-type')

    if content:
        ctype, pdict = cgi.parse_header(content)
        # refuse to receive non-json content
        if ctype == 'application/json':
            error = False

    if not error:
        error = True
        # read the message and convert it into a python dictionary
        length = int(server.headers.get('content-length'))
        data_string = server.rfile.read(length).decode('utf-8')
        data = json.loads(data_string) if data_string else None

        if data and password_field_json in data and username_field_json in data and len(data) == 2:
            username = data[username_field_json]
            password = data[password_field_json]
            found, error = check_user(username, False, None)
            if not error and not found:
                error = insert_user(username, password)
            if not error:
                server._set_headers()
                json_string = json.dumps({'username_exist': found})
                server.wfile.write(json_string.encode(encoding='utf_8'))

    if error:
        server.send_response(HTTPStatus.BAD_REQUEST.value)
        server.end_headers()