import sqlite3
import os
import sys 
from datetime import datetime
from src.database.db_manager import DatabaseManager

class TransactionManager(DatabaseManager):
    def __init__(self, db_path = None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        pass  # Ініціалізація бази даних, створення таблиць, якщо вони не існують