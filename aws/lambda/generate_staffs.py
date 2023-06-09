from src.log_module import create_logger
from src.faker.generator import generate_staffs
from src.db.db_utils import DatabaseObject, upload_file

logger = create_logger()
db_obj = DatabaseObject()

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
    store_id_params = event['store_id']

    # Validate store_id
    db_obj.connect()
    available_store_ids = [row[0] for row in db_obj.fetch("select id from dim_db.stores")]
    
    if store_id_params not in available_store_ids:
        logger.error("provided store id does not exist in database")
        return {
            "statusCode": 400,
            "message": 'Bad Request'
        }

    # generate staffs
    data = generate_staffs(store_id=store_id_params, n=num_recs_params)

    # upload to postgres
    try:
        response = upload_file(db_obj, data, schema='dim_db', table='staffs')
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
    "num_recs": "1",
    "store_id": <store_id>
}

'''
