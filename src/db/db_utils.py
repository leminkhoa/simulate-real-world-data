import yaml
import os
import psycopg2
from jinja2 import Environment, FileSystemLoader, select_autoescape


class DatabaseObject(object):
    user            =   os.environ.get('DB_USER' ,      'test'      )
    password        =   os.environ.get('DB_PASSWORD',   'test'      )
    host            =   os.environ.get('DB_HOSTNAME',   'localhost' )
    database        =   os.environ.get('DB_DATABASE',   'test'      )
    port            =   os.environ.get('DB_PORT',       '5432'      )
    
    def __init__(self):
        self.conn = psycopg2.connect(
                            user=self.user,
                            password = self.password,
                            host = self.host,
                            database = self.database,
                            port = self.port)
        self.cur = self.conn.cursor()

    def execute(self, query):
        # Create table to insert
        self.cur.execute(query)
        self.conn.commit()
    
    def close_conn(self):
        self.cur.close()
        self.conn.close() 
    
def generate_sql_queries(db_config, template_folder):
    env = load_template(template_folder)
    sql_queries = []
    for step in db_config['steps']:
        template = env.get_template(f"{step['template']}.sql.jinja")
        sql_queries.append(template.render(**step['data']))
    return sql_queries
        

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
