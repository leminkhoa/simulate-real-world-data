import os

import yaml
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
