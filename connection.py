import pymysql

from config import db

def get_connection():
    return pymysql.connect(
        host         = db['host'],
        port         = db['port'],
        user         = db['user'],
        password     = db['password'],
        db           = db['database'],
        charset      = 'utf8mb4',
        autocommit   = False
)
