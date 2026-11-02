import sqlite3
import os
import sys 
from datetime import datetime
from src.database.db_manager import DatabaseManager
from contextlib import closing

class FoodKkalManager(DatabaseManager):
    def __init__(self, db_path = None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_kkal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                mass REAL NOT NULL,
                kkal REAL NOT NULL,
                protein REAL NOT NULL,
                sacharidy REAL NOT NULL,
                fat REAL NOT NULL,
                date_added TEXT NOT NULL,
                comment TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_product(self, product, mass, kkal, protein, sacharidy, fat, comment=None):
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO food_kkal (product, mass, kkal, protein, sacharidy, fat, date_added, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product, mass, kkal, protein, sacharidy, fat, date_added, comment))
            print("---------------------------------------------------\n"
                  f"Продукт '{product}' успішно доданий до бази даних.\n"
                  "---------------------------------------------------\n")
            conn.commit()

    def get_all_products(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM food_kkal')
            return cursor.fetchall()

    def get_total_calories_today(self, date=None):
        """Потрібно брати дані за конкретний день, а не за всі дні"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(kkal) AS total_kkal, " \
                                  "SUM(protein) AS total_protein, " \
                                  "SUM(sacharidy) AS total_sacharidy, " \
                                  "SUM(fat) AS total_fat " \
                            "FROM food_kkal WHERE date(date_added) = date(?)", (date,))
            return cursor.fetchone()

    def delete_product(self, product_id):
        """Видаляє продукт з бази даних за його ID"""
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM food_kkal WHERE id = ?", (product_id,)) 
            conn.commit()

    def edit_product(self, product_id, product, mass, kkal, protein, sacharidy, fat, comment=None):
        """Редагує продукт у базі даних за його ID"""
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE food_kkal
                SET product = ?, mass = ?, kkal = ?, protein = ?, sacharidy = ?, fat = ?, comment = ?
                WHERE id = ?
            ''', (product, mass, kkal, protein, sacharidy, fat, comment, product_id))
            conn.commit()