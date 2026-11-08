
"""
    Сервіси програми, логіка 

    add_product(product,mass,kkal,protein,sacharidy,fat) - перераховує 100 грамів на порцію, вводимо дані на 100 грамів а запис і вивід порції

    get_all_products() - повертає список продуктів з бази даних

    get_total_calories() - повертає загальну кількість калорій, білків, вуглеводів та жирів за сьогоднішній день
"""

from src.database.FoodKkal import FoodKkalManager
from src.database.products_db import ProductsManager

class FoodService:
    def __init__(self):
        self.food_manager = FoodKkalManager()
        self.product_manager = ProductsManager()

    def add_product(self,product,mass,kkal,protein,carbs,fat):
        # Зберігаємо продукт в довідник продуктів (product_db)
        # в цій перемінні буде id первинного ключа продукта щоб достати ім'я продукта    
        product_id = self.product_manager.add_product(product, None, kkal, protein, carbs, fat, is_active = 'True')
        
        total_kkal = (kkal * mass) / 100
        total_protein = (protein * mass) / 100
        total_sacharidy = (carbs * mass) / 100
        total_fat = (fat * mass) / 100


        self.food_manager.add_product(product_id, mass, total_kkal, total_protein, total_sacharidy, total_fat)

    def edit_product(self, product_id, product, mass, kkal, protein, sacharidy, fat):
        """ Редагування запису"""
        total_kkal = (kkal * mass) / 100
        total_protein = (protein * mass) / 100
        total_sacharidy = (sacharidy * mass) / 100
        total_fat = (fat * mass) / 100

        self.food_manager.edit_product(product_id, product, mass, total_kkal, total_protein, total_sacharidy, total_fat)

    def get_all_products(self):
        # Повертає список продуктів з бази даних
        return self.food_manager.get_all_products()

    def get_total_calories_today(self):
        # Повертає загальну кількість калорій, білків, вуглеводів та жирів за сьогоднішній день
        # Можна використати для повернення тільки калорій.
        return self.food_manager.get_total_calories_today()


    def delete_product(self, product_id):
        # Видаляє продукт з бази даних за його ID
        self.food_manager.delete_product(product_id)

    def edit_record(self, product_id):
        # Редагування запису
        self.food_manager.edit_product(product_id)



# ------------------------------------------------------------
# Інтеграція Ші
from src.ai.AiService import AiService

ai = AiService(api_key="YOUR_API")

#result = ai.analyze_food_label("photo")

#if result:
    # print("ШІ успішно розпізнав:")
    # print(f"Назва: {result['product_name']}")
    # print(f"Калорії: {result['kkal']}")
    # print(f"Білки: {result['protein']}")
    # print(f"Вуглеводи: {result['sacharidy']}")
    # print(f"Жири: {result['fat']}")
    








