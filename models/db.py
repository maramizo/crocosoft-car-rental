from flask import _app_ctx_stack
from MySQLdb import connect
from config import ENVIRONMENT_VARIABLES


def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'mysql_db'):
        top.mysql_db = connect(
            host=ENVIRONMENT_VARIABLES.DATABASE_HOST,
            port=ENVIRONMENT_VARIABLES.DATABASE_PORT,
            user=ENVIRONMENT_VARIABLES.DATABASE_USER,
            passwd=ENVIRONMENT_VARIABLES.DATABASE_PASSWORD,
            db=ENVIRONMENT_VARIABLES.DATABASE_NAME
        )
    return top.mysql_db