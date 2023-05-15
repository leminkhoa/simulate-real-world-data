import json
import sys
sys.path.append('../..')
from src.log_module import create_logger
from src.faker.generator import generate_stores
from src.db.db_utils import DatabaseObject, upload_file

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
    # generate stores
    data = generate_stores(num_recs_params)
    # upload to postgres
    try:
        response = upload_file(db_obj, data, schema='dim_db', table='stores')
    except Exception as error:
        logger.error(error)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "message": 'Internal Server Error'
        }


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "insertedRow": response
    }


'''
# ===== Test Event ==== 

event = {
    "queryStringParameters": {
        "num_recs": 5
    }
}

'''
