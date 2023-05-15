import yaml
import os
import psycopg2
from psycopg2.extensions import AsIs
from jinja2 import Environment, FileSystemLoader, select_autoescape


class DatabaseObject(object):
    
    def __init__(self):
        self.user       =   os.environ.get('DB_USER' ,      'postgres'      )
        self.password   =   os.environ.get('DB_PASSWORD',   'abc'           )
        self.host       =   os.environ.get('DB_HOSTNAME',   'localhost'     )
        self.database   =   os.environ.get('DB_DATABASE',   'operation'      )
        self.port       =   os.environ.get('DB_PORT',       '5432'          )    

    def connect(self):
        self.conn = psycopg2.connect(
                            user=self.user,
                            password = self.password,
                            host = self.host,
                            database = self.database,
                            port = self.port
                        )
        self.cur = self.conn.cursor()

    def execute(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def fetch(self, query, size=100):
        self.cur.execute(query)
        row = self.cur.fetchmany(size)
        return row
    
    def insert(self, data, schema, table_name):
        sql = f'''INSERT INTO {schema}.{table_name} (%s) values %s'''
        success_recs = 0
        for row in data:
            try:
                self.cur.execute(
                sql, 
                    (
                        AsIs(','.join(row.keys())), 
                        tuple(row.values())
                    )
                )
            except Exception:
                continue
            success_recs +=1
        self.conn.commit()
        return success_recs

    
    def close_conn(self):
        self.cur.close()
        self.conn.close() 


def generate_sql_queries(db_folder: str, config_path: str, template_folder: str):
    env = load_template(os.path.join(db_folder, template_folder))
    db_config = parse_yaml(db_folder, config_path)

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


def upload_file(db_obj, data, schema, table):
    """Upload data to postgres database

    Args:
        db_obj (psycopg2.connection): database object
        data (dict): data to upload
        table (str): table to upload data to

    Returns:
        str: json response
    """
    db_obj.connect()
    success_recs = db_obj.insert(data, schema, table)
    db_obj.close_conn()

    return success_recs