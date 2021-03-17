from http.server import HTTPServer
from Server_Main import *

port = 8080

def run():
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)

    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()