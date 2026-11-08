import sqlite3
import logging

logger = logging.getLogger(__name__)

def db_safe(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except sqlite3.Error as e:
            logger.error(f"Помилка БД у функції {func.__name__}: {e}")
            return None
    return wrapper