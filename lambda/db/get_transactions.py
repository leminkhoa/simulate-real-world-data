import json
from src.log_module import create_logger
from src.db.db_utils import DatabaseObject

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
  
    # fetch metadata from database
    transactions = db_obj.fetch_and_process("SELECT * FROM transaction_db.transactions", None)
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "data": transactions,
        "numberOfRecords": len(transactions)
    }
