import json
import cgi

def send_error(server, code):
    server.send_response(code)
    server.end_headers()

def send_json(server, dict):
    server._set_headers()
    json_string = json.dumps(dict)
    server.wfile.write(json_string.encode(encoding='utf_8'))

def read_json_convert_to_dictionary(server):
    error = True
    dictionary = None

    content = server.headers.get('content-type')

    if content:
        ctype, pdict = cgi.parse_header(content)
        # refuse to receive non-json content
        if ctype == 'application/json':
            error = False

    if not error:
        # read the message and convert it into a python dictionary
        length = int(server.headers.get('content-length'))
        data_string = server.rfile.read(length).decode('utf-8')
        if data_string:
            dictionary = json.loads(data_string)
        else:
            error = True

    return error, dictionary
