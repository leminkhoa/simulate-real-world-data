from src.db import db_utils
from src.log_module import create_logger

logger = create_logger()

if __name__ == '__main__':
    db_obj = db_utils.DatabaseObject()
    db_obj.connect()
    logger.info("Successfully connected to database '{db_host}-{db}'".format(db_host=db_obj.host, db=db_obj.database.upper()))
    # Generate db queries
    db_setup_queries = db_utils.generate_sql_queries(
                                    db_folder='src/db',
                                    config_path='db_init.yml',
                                    template_folder='templates'
                                )
    # Execute set up
    for query in db_setup_queries:
        logger.info("Execute query: \n{query}\n".format(query=query))
        db_obj.execute(query)
    
    db_obj.close_conn()
    logger.info("Task finished, Connection closed!")
