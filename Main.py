from http.server import HTTPServer
from Server_Main import *
from threading import Lock

port = 8080
samples_mutex = Lock()
model_mutex = Lock()
training_model_mutex = Lock()

def run():
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)

    httpd.serve_forever()

if __name__ == '__main__':
    run()