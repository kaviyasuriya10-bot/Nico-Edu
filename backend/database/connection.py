from contextlib import contextmanager
import pymysql  # type: ignore[reportMissingModuleSource]
from pymysql.cursors import DictCursor  # type: ignore[reportMissingModuleSource]
from config import settings

@contextmanager
def get_db():
    conn = pymysql.connect(host=settings.database_host, port=settings.database_port,
        user=settings.database_user, password=settings.database_password, database=settings.database_name,
        cursorclass=DictCursor, autocommit=False, charset='utf8mb4')
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def rows(cursor):
    return cursor.fetchall()
