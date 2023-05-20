import boto3
import json
import os
import random
from src.log_module import create_logger
from src.faker.generator import generate_transactions
from src.db.db_utils import DatabaseObject
from src.utils import get_current_datetime, parse_num_recs

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

    db_obj.connect()
    # params from event body
    num_recs_params = event['num_recs']

    # parse
    try:
        num_recs_params = parse_num_recs(num_recs_params)
        # random value
        if isinstance(num_recs_params, list):
            num_recs_params = random.randint(num_recs_params[0], num_recs_params[1])
    except Exception:
        return {
            "statusCode": 400,
            "message": 'Bad Request'
        }
    
    # fetch metadata from database
    customers = db_obj.fetch_and_process("SELECT * FROM dim_db.customers", 'customer_id')
    stores = db_obj.fetch_and_process("SELECT * FROM dim_db.stores", 'id')
    staffs = db_obj.fetch_and_process("SELECT * FROM dim_db.staffs", 'staff_id')
    products = db_obj.fetch_and_process("SELECT * FROM dim_db.products", 'product_id')

    # generate transactions
    data = generate_transactions(stores, customers, staffs, products, 5, 2, num_recs_params)
    db_obj.close_conn()

    # define s3 params
    bucket_name     = os.environ.get('S3_RAW_LAYER_BUCKET')
    directory_name  = '{table}/year={year}/month={month}/day={day}/table_{year}{month}{day}_{hour}{minute}{second}.json'
    ts = get_current_datetime()

    directory_name= directory_name.format(
            table='tb_transactions',
            year=ts.strftime('%Y'),
            month=ts.strftime('%m'),
            day=ts.strftime('%d'),
            hour=ts.strftime('%H'),
            minute=ts.strftime('%M'),
            second=ts.strftime('%S'),
        )

    # upload to s3
    try:
        s3 = boto3.resource('s3')
        s3object = s3.Object(
            bucket_name, 
            directory_name
        )
    
        s3object.put(
            Body=(bytes(json.dumps(data).encode('UTF-8')))
        )
    except Exception as error:
        logger.error(error)
        return {
            "statusCode": 500,
            "message": 'Internal Server Error'
        }
    
    return {
        "statusCode": 200,
        "s3Location": f"s3://{bucket_name}/{directory_name}",
        "numberOfRecords": len(data)
    }

'''
# ===== Test Event ==== 

{
    "num_recs": "[2-15]"
}

'''
