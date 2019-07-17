import itertools


def is_number(string):
    """
    Checks if a string is a number regardless of format
    :param string: will check
    :return: True or False
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def to_simple_list(complex_list):
    """
    Create simple list from complex list
    :param complex_list: list of the following format [[x0, x1], [y1, y2]]
    :return: simple list of the following format [x0, x1, y1, y2]
    """
    return list(itertools.chain(*complex_list))


def create_list(size_list):
    """
    Need if meet list with '('. Remove '(' and create simple list
    :param size_list: list with '('
    :param exist: Does exist list with '('
    :return: list without '()'
    """
    new_size_list = [i.split(' ') for i in size_list]
    for in_item in range(len(new_size_list)):
        new_size_list[in_item][1] = new_size_list[in_item][1][1:-1]
    return new_size_list


def width_to_size(size_list):
    """
    Create valid list without 'width' and similar
    :param size_list:
    :return: list without 'width' and similar
    """
    new_size_list = []
    for item in size_list:
        if item.startswith('Width: D (Standard);'):
            item = item.replace('Width: D (Standard); Size: ', '')
            new_size_list.append(item)
        if item.endswith(';'):
            item = item.replace(';', '')
            new_size_list.append(item)
    return new_size_list
