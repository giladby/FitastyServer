import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
import json
import cgi

username_field_json = 'username'
password_field_json = 'password'
username_field_mysql = 'username'
password_field_mysql = 'password'
users_table_mysql = 'users'
port = 8080

class MySQLConnectionFields:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

class Server(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.operations_dict_get = self.set_operations_dict_get()
        self.operations_dict_post = self.set_operations_dict_post()
        super().__init__(request, client_address, server)

    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def set_operations_dict_get(self):
        return {"/users": self.users_get}

    def set_operations_dict_post(self):
        return {"/users": self.users_post}

    def users_get(self):
        print("in users get")
        error = True
        result = None

        qs = parse_qs(urlparse(self.path).query)
        if username_field_json in qs and password_field_json in qs:
            username = qs[username_field_json][0]
            password = qs[password_field_json][0]
            result, error = check_user(username, True, password)
        if not error:
            self._set_headers()
            json_string = json.dumps({'found': result})
            self.wfile.write(json_string.encode(encoding='utf_8'))
        else:
            self.send_response(HTTPStatus.BAD_REQUEST.value)
            self.end_headers()

    def users_post(self):
        print("in users post")
        error = True
        content = self.headers.get('content-type')

        if content:
            ctype, pdict = cgi.parse_header(content)
            # refuse to receive non-json content
            if ctype == 'application/json':
                error = False

        if not error:
            error = True
            # read the message and convert it into a python dictionary
            length = int(self.headers.get('content-length'))
            data_string = self.rfile.read(length).decode('utf-8')
            data = json.loads(data_string) if data_string else None

            if data and password_field_json in data and username_field_json in data:
                username = data[username_field_json]
                password = data[password_field_json]
                found, error = check_user(username, False, None)
                if not error and not found:
                    error = insert_user(username, password)

        status = HTTPStatus.BAD_REQUEST.value if error else HTTPStatus.OK.value

        self.send_response(status)
        self.end_headers()

    def operate_by_operations_dict(self, operations_dict):
        sub = urlparse(self.path).path
        if sub in operations_dict:
            operations_dict.get(sub)()
        else:
            self.send_response(HTTPStatus.BAD_REQUEST.value)
            self.end_headers()

    # GET checks if the user exist in system
    def do_GET(self):
        print("in get")
        operations = self.operations_dict_get
        self.operate_by_operations_dict(operations)

    # POST creates user in system
    def do_POST(self):
        print("in post")
        operations = self.operations_dict_post
        self.operate_by_operations_dict(operations)

def get_db_fields():
    host = "fitasty-db.cc4qtocqbg7k.us-east-2.rds.amazonaws.com"
    host = "127.0.0.1"
    user = "admin"
    user = "root"
    password = "epsilonEP2"
    password = "123456"
    database = "fitasty"
    database = "fitasty_demo"
    return MySQLConnectionFields(host, user, password, database)

def get_mysql_connection(mysql_fields):
    return mysql.connector.connect(
        host=mysql_fields.host,
        user=mysql_fields.user,
        passwd=mysql_fields.password,
        database=mysql_fields.database)

def iter_row(cursor, size=10):
    #running example:
    #cursor.execute("SELECT * FROM users")
    #    for row in iter_row(cursor, 10):
    #        print(row)
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def handle_error():
    print("Error trying access mysql records")

def get_user_query(cursor, username, check_password, password):
    found = False
    error = True
    if cursor:
        try:
            query = f"SELECT * FROM {users_table_mysql} WHERE {username_field_mysql}='{username}'"
            if check_password:
                query += f" AND {password_field_mysql}='{password}'"
            cursor.execute(query)
            if cursor.fetchone():
                found = True
            error = False
        except:
            handle_error()
    return found, error

def insert_user_query(conn, cursor, username, password):
    error = False
    if cursor:
        try:
            query = f"INSERT INTO {users_table_mysql} ({username_field_mysql}, {password_field_mysql}) VALUES (%s, %s)"
            val = (username, password)
            cursor.execute(query, val)

            conn.commit()
        except:
            handle_error()
            error = True
    return error

def close_connection(conn, cursor):
    if conn is not None:
        conn.close()
    if cursor is not None:
        cursor.close()

def get_mysql_cursor():
    conn = None
    cursor = None
    error = False
    try:
        db_fields = get_db_fields()
        conn = get_mysql_connection(db_fields)
        cursor = conn.cursor()
    except:
       handle_error()
       error = True
    return conn, cursor, error

def check_user(username, check_user, password):
    conn, cursor, error = get_mysql_cursor()
    result = None
    if not error:
        result, error = get_user_query(cursor, username, check_user, password)
    close_connection(conn, cursor)
    return result, error

def insert_user(username, password):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = insert_user_query(conn, cursor, username, password)
    close_connection(conn, cursor)
    return error

def run():
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)

    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()