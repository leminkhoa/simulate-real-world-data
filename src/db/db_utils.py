import os
import psycopg2
from psycopg2.extensions import AsIs
from src import utils

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
    
    def fetch_all(self, query):
        self.cur.execute(query)
        row = self.cur.fetchall()
        return row
    
    def fetch_as_json(self, query, key_col):
        self.cur.execute(query)
        row = self.cur.fetchall()
        col_names = [col.name for col in self.cur.description]
        
        def _create_dict(data, col_names, key_col):
            key_index = col_names.index(key_col)
            result = {}
            for row in data:
                key = row[key_index]
                customer_data = {}
                for i in range(len(col_names)):
                    if i != key_index:
                        customer_data[col_names[i]] = row[i]
                result[key] = customer_data
            return result
        
        return _create_dict(row, col_names, key_col)
    
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
    env = utils.load_template(os.path.join(db_folder, template_folder))
    db_config = utils.parse_yaml(db_folder, config_path)

    sql_queries = []
    for step in db_config['steps']:
        template = env.get_template(f"{step['template']}.sql.jinja")
        sql_queries.append(template.render(**step['data']))
    return sql_queries


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
