from http.server import BaseHTTPRequestHandler
from Server_Users_Handling import *
from Server_Food_Handling import *

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
                "/users/check_username": self.check_username,
                "/users/get_account_info": self.get_account_info,
                "/food/get_foods": self.get_foods,
                "/foods/get_ingredient_info": self.get_ingredient_info,
                "/foods/get_dish_info": self.get_dish_info}

    def set_operations_dict_post(self):
        return {"/users/insert_account": self.insert_account,
                "/users/update_account": self.update_account,
                "/foods/insert_ingredient": self.insert_ingredient,
                "/foods/insert_dish": self.insert_dish}

    def get_dish_info(self):
        server_get_dish_info(self)

    def insert_dish(self):
        server_insert_dish(self)

    def get_ingredient_info(self):
        server_get_ingredient_info(self)

    def get_foods(self):
        server_get_foods(self)

    def insert_ingredient(self):
        server_insert_ingredient(self)

    def get_account_info(self):
        server_get_account_info(self)

    def check_username(self):
        server_check_username(self)

    def update_account(self):
        server_update_account(self)

    def log_in(self):
        server_log_in(self)

    def insert_account(self):
        server_insert_account(self)

    def operate_by_operations_dict(self, operations_dict):
        sub = urlparse(self.path).path
        if sub in operations_dict:
            operations_dict.get(sub)()
        else:
            send_error(self, HTTPStatus.BAD_REQUEST.value)

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