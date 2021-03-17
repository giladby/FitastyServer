from http.server import BaseHTTPRequestHandler
from Server_Users_Handling import *

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
        return {"/users/log_in": self.log_in,
                "/users/check_username": self.check_username}

    def set_operations_dict_post(self):
        return {"/users/insert_account": self.insert_account}

    def check_username(self):
        server_check_username(self)

    def log_in(self):
        server_log_in(self)

    def insert_account(self):
        server_insert_account(self)

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