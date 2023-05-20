from src.log_module import create_logger
from src.faker.generator import generate_customers
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
    num_recs_params = int(event['num_recs'])

    # generate customers
    data = generate_customers(num_recs_params)
    
    # upload to postgres
    try:
        response = upload_file(db_obj, data, schema='dim_db', table='customers')
    except Exception as error:
        logger.error(error)
        return {
            "statusCode": 500,
            "message": 'Internal Server Error'
        }


    return {
        "statusCode": 200,
        "insertedRow": response
    }


'''
# ===== Test Event ==== 

{
    "num_recs": "1"
}

'''