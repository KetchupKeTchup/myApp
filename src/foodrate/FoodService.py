
"""
    Сервіси програми, логіка 

    add_product(product,mass,kkal,protein,sacharidy,fat) - перераховує 100 грамів на порцію, вводимо дані на 100 грамів а запис і вивід порції

    get_all_products() - повертає список продуктів з бази даних

    get_total_calories() - повертає загальну кількість калорій, білків, вуглеводів та жирів за сьогоднішній день
"""

from src.database.FoodKkal import FoodKkalManager

class FoodService:
    def __init__(self):
        self.food_manager = FoodKkalManager()

    def add_product(self,product,mass,kkal,protein,sacharidy,fat):
        total_kkal = (kkal * mass) / 100
        total_protein = (protein * mass) / 100
        total_sacharidy = (sacharidy * mass) / 100
        total_fat = (fat * mass) / 100

        self.food_manager.add_product(product, mass, total_kkal, total_protein, total_sacharidy, total_fat)

    def get_all_products(self):
        # Повертає список продуктів з бази даних
        return self.food_manager.get_all_products()

    def get_total_calories_today(self):
        # Повертає загальну кількість калорій, білків, вуглеводів та жирів за сьогоднішній день
        # Можна використати для повернення тільки калорій.
        return self.food_manager.get_total_calories_today()

    def get_calories_protein_for_dashboard(self):
        # Повертає загальну кількість калорій та білків за сьогоднішній день
        return self.food_manager.get_calories_protein_for_dashboard()




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
    








