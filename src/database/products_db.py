import logging
from datetime import datetime
from src.database.db_manager import DatabaseManager
from contextlib import closing

logger = logging.getLogger(__name__) # Має бути створений поза класом

class ProductsManager(DatabaseManager):
    
    def __init__(self, db_path = None):
        super().__init__(db_path)
        self.init_db()

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                baracode TEXT,
                kkal REAL NOT NULL,
                protein REAL NOT NULL,
                carbs REAL NOT NULL,
                fat REAL NOT NULL,
                is_active TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_product(self,product_name,baracode,kkal,protein,carbs,fat,is_active):
        logger.info("Початок роботи додавання продукту до products_db")
        
        try:
            with closing(self.get_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute('''
                    INSERT INTO products_db(product,baracode,
                    kkal,protein,carbs,fat,is_active) VALUES(?,?,?,?,?,?,?)
                ''', (product_name,baracode,kkal,protein,carbs,fat,is_active))
                conn.commit()
                logger.info(f"Продукт успішно доданий.  назва: {product_name}")
                
                # Повернення автокрімента - первичного ключа
                return cursor.lastrowid
        
        except Exception:
            logger.exception(
                f"Помилка під час додавання продукту в product_db {product_name}",
                product_name
            )
            return None

    