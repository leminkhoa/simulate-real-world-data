import os
import random
import yaml
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_template(template_folder='templates'):
    env = Environment(
        loader=FileSystemLoader(template_folder),
        autoescape=select_autoescape()
    )
    return env


def parse_yaml(folder, filename):
    reader = read_file(folder, filename)
    config = yaml.safe_load(reader)
    return config


def read_file(folder, filename):
    with open(os.path.join(folder, filename), 'r') as f:
        return f.read()


def filter_dict(data: dict, filter_key: list):
    '''Filter dictionary by key'''
    return { k: v for k,v in data.items() if k in filter_key }


def rename_keys(dictionary, mapping):
    for old_key in mapping:
        new_key = mapping[old_key]
        dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


def random_int(start, end):
    min = end
    for _ in range(start+2):
        result = random.randint(start, end)
        if min >= result:
            min = result
    return min


def get_current_str_datetime():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def get_current_datetime():
    return datetime.now(timezone.utc)


def parse_variable(var):
    if isinstance(var, datetime):
        return var.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return var


def parse_num_recs(num_recs: str):
    """If num_recs is a list in string format, return list. Else return integer
    """
    if num_recs.startswith('[') and num_recs.endswith(']'):
        try:
            num_recs = num_recs[1:-1]
            num_recs = num_recs.split('-')
            num_recs = [int(x) for x in num_recs]
            
            if len(num_recs) != 2:
                raise ValueError("Number of records should only have two elements for start and end range")
            
            if num_recs[0] >= num_recs[1]:
                raise ValueError("Start must be smaller than end")
            
            return num_recs
            
        except ValueError as e:
            raise e
        
    else:
        return int(num_recs)
