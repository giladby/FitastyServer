from http.server import BaseHTTPRequestHandler
from Server_Users_Handling import *
from Server_Food_Handling import *
from Server_Diet_Diaries_Handling import *
from Server_Demo import *

class Server(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.operations_dict_get = self.set_operations_dict_get()
        self.operations_dict_post = self.set_operations_dict_post()
        self.operations_dict_delete = self.set_operations_dict_delete()
        self.operations_dict_put = self.set_operations_dict_put()
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
                "/foods/get_ingredient_info": self.get_ingredient_info,
                "/foods/get_dish_info": self.get_dish_info,
                "/users/get_calorie_info": self.get_calorie_info,
                "/diet_diaries/get_diet_diary": self.get_diet_diary,
                "/diet_diaries/get_diet_diaries": self.get_diet_diaries}

    def set_operations_dict_post(self):
        return {"/users/insert_account": self.insert_account,
                "/foods/insert_ingredient": self.insert_ingredient,
                "/foods/get_foods": self.get_foods,
                "/foods/insert_dish": self.insert_dish,
                "/diet_diaries/insert_diet_diary": self.insert_diet_diary,
                "/json_echo": self.json_echo}

    def json_echo(self):
        server_json_echo(self)

    def set_operations_dict_delete(self):
        return {"/users/delete_account": self.delete_account,
                "/diet_diaries/delete_diet_diary": self.delete_diet_diary}

    def set_operations_dict_put(self):
        return {"/users/update_account": self.update_account,
                "/diet_diaries/update_diet_diary": self.update_diet_diary}

    def update_diet_diary(self):
        server_update_diet_diary(self)

    def delete_diet_diary(self):
        server_delete_diet_diary(self)

    def get_diet_diary(self):
        server_get_diet_diary(self)

    def get_diet_diaries(self):
        server_get_diet_diaries(self)

    def insert_diet_diary(self):
        server_insert_diet_diary(self)

    def get_calorie_info(self):
        server_get_calorie_info(self)

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

    def delete_account(self):
        server_delete_account(self)

    def insert_account(self):
        server_insert_account(self)

    def operate_by_operations_dict(self, operations_dict):
        sub = urlparse(self.path).path
        try:
            operations_dict.get(sub)()
        except:
            send_error(self, HTTPStatus.BAD_REQUEST.value)

    def do_GET(self):
        print("in get")
        operations = self.operations_dict_get
        self.operate_by_operations_dict(operations)

    def do_POST(self):
        print("in post")
        operations = self.operations_dict_post
        self.operate_by_operations_dict(operations)

    def do_PUT(self):
        print("in put")
        operations = self.operations_dict_put
        self.operate_by_operations_dict(operations)

    def do_DELETE(self):
        print("in put")
        operations = self.operations_dict_delete
        self.operate_by_operations_dict(operations)