from src.log_module import create_logger
from src.faker.generator import generate_transactions
from src.db.db_utils import DatabaseObject

logger = create_logger()

db_obj = DatabaseObject()

db_obj.connect()

customers = db_obj.fetch_as_json("SELECT * FROM dim_db.customers", 'customer_id')
stores = db_obj.fetch_as_json("SELECT * FROM dim_db.stores", 'id')
staffs = db_obj.fetch_as_json("SELECT * FROM dim_db.staffs", 'staff_id')
products = db_obj.fetch_as_json("SELECT * FROM dim_db.products", 'product_id')

result = generate_transactions(stores, customers, staffs, products, 5, 2)
print(result)
