import json
from src.log_module import create_logger
from src.faker.generator import generate_transactions
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

    db_obj.connect()
    # params from event body
    num_recs_params = event['queryStringParameters']['num_recs']
    
    # fetch metadata from database
    customers = db_obj.fetch_and_process("SELECT * FROM dim_db.customers", 'customer_id')
    stores = db_obj.fetch_and_process("SELECT * FROM dim_db.stores", 'id')
    staffs = db_obj.fetch_and_process("SELECT * FROM dim_db.staffs", 'staff_id')
    products = db_obj.fetch_and_process("SELECT * FROM dim_db.products", 'product_id')

    # generate transactions
    data = generate_transactions(stores, customers, staffs, products, 5, 2, num_recs_params)
    success_recs = 0
    for row in data:
        # upload to postgres
        try:
            db_obj.cur.execute('''
                INSERT INTO transaction_db.transactions
                SELECT %s, %s, %s, %s, array_agg(elem), %s, %s, %s
                FROM jsonb_array_elements(%s::jsonb) AS elem
                ''',
                (
                    row['transaction_id'],
                    json.dumps(row['store']),
                    json.dumps(row['customer']),
                    json.dumps(row['staff']),
                    json.dumps(row['purchased_number_items']),
                    row['total_amount'],
                    row['utc_dt'],
                    json.dumps(row['transaction']),
                )
            )
        except Exception as error:
            logger.error(error)
            continue
        success_recs+=1
    db_obj.conn.commit()
    db_obj.close_conn()
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "insertedRow": success_recs
    }

'''
# ===== Test Event ==== 

event = {
    "queryStringParameters": {
        "num_recs": 5
    }
}

'''
