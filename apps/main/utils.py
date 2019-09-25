import re


def get_number_from_string(string=''):
    sizes = re.findall(r'\d+', string)
    return sizes
