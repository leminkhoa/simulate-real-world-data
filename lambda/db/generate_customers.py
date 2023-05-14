import json
import sys
sys.path.append('../..')
from src.log_module import create_logger
from src.faker.generator import *
from src.db.db_utils import DatabaseObject

logger = create_logger()

def lambda_handler(event, context):
    """Lambda handler

    Args:
        event (dict): event data
        context (dict): context data

    Returns:
        dict: lambda response
    """
    db_obj = DatabaseObject()
    
    # params from event body
    num_recs_params = event['queryStringParameters']['num_recs']
    table = 'customers'
    schema = 'dim_db'
    # generate customers
    data = generate_customers(num_recs_params)
    # upload to postgres
    response = upload_file(db_obj, data, schema, table)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "insertedRow": response
    }


def upload_file(db_obj, data, schema, table):
    """Upload data to postgres database

    Args:
        db_obj (psycopg2.connection): database object
        data (dict): data to upload
        table (str): table to upload data to

    Returns:
        str: json response
    """
    try:
        db_obj.connect()
        success_recs = db_obj.insert(data, schema, table)
    except Exception as error:
        logger.error(error)
    return success_recs

'''
# ===== Test Event ==== 

event = {
    "queryStringParameters": {
        "num_recs": 100
    }
}

'''