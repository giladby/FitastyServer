import csv
import os
from distutils.util import strtobool

def convert_boolean_to_number(boolean):
    return 1 if boolean else 0

def convert_str_to_boolean(boolean_str):
    return bool(strtobool(boolean_str))

def write_rows_to_file(rows, file_path, write):
    error = False
    try:
        with open(file_path, 'w' if write else 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    except:
        error = True
    return error

def is_file_exist(file_name):
    return os.path.isfile(file_name)

def create_path_if_needed(full_path):
    os.makedirs(os.path.dirname(full_path), exist_ok=True)