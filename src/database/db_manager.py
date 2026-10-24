import sqlite3
import os
import sys 
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "database.db")

class DatabaseManager:
    def __init__(self, db_path=None): 
        # db_path = None, це патрн у пайтоні, рахується добрим тоном. Коли вкзано None, це означає що цей параметр не обов'язковий
        # це дозволяє дозволяє створювати об'єкт двома способами: з вказаним шляхом до бази даних або без нього, використовуючи значення за замовчуванням. Помітка 1
        self.db_path = db_path or DB_PATH

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Помилка підключення до бази даних: {e}")
            sys.exit(1)



