import distutils.util


def convert_boolean_to_number(boolean):
    return 1 if boolean else 0

def convert_str_to_boolean(boolean_str):
    return bool(distutils.util.strtobool(boolean_str))