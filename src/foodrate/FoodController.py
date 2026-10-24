from src.foodrate.FoodService import FoodService
from src.foodrate.FoodUi import FoodUi


class FoodController:
    def __init__(self):
        self.service = FoodService()
        self.ui = FoodUi()

    def start(self):
        # Запуск логіки меню харчування
        while True:
            action = self.ui.display_menu_food()

            if action == "1":
                # 1. Просимо UI зібрати дані
                product_data = self.ui.get_product_data()
                
                if product_data is not None:
                    self.service.add_product(*product_data)
                    self.ui.show_message("Продукт успішно додано!")
                else:
                    self.ui.show_message("Помилка при додаванні продукту.")

            elif action == "2":
                products = self.service.get_all_products()
                self.ui.show_products(products)

            elif action == "3":
                total_calories = self.service.get_total_calories()
                self.ui.show_total_calories(total_calories)

            elif action == "0":
                print("Вихід в головне меню.")
                break

            else:
                print("Некоректна дія. Спробуйте ще раз.")

    def handle_add_product(self, product, mass, kkal, protein, sacharidy, fat): 
        
        # 1. Передає дані в сервіс для обрахунку та збереження
        self.service.add_product(product, mass, kkal, protein, sacharidy, fat)
        print("Продукт успішно додано!")

    def handle_view_products(self):       
        
        # 1. Просить сервіс дістати дані з БД
        products = self.service.get_all_products()
        
        # 2. Передає ці дані в UI, щоб він їх намалював
        self.ui.show_products(products)

    def handle_total_calories(self):
        
        # 1. Просить сервіс дістати дані з БД
        total_calories = self.service.get_total_calories()
        
        # 2. Передає ці дані в UI, щоб він їх намалював
        self.ui.show_total_calories(total_calories)

    def handle_total_calories_only(self):
        
        # 1. Просить сервіс дістати дані з БД
        total_calories_only = self.service.get_total_calories_only()
        
        # 2. Передає ці дані в UI, щоб він їх намалював
        self.ui.show_total_calories(total_calories_only)

    def show_dashboard_data(self):
        # 1. Просить сервіс дістати дані з БД
        total_calories, total_protein = self.service.get_calories_protein_for_dashboard()
        # 2. Передає ці дані в UI, щоб він їх намалював
        self.ui.dashboard(total_calories, total_protein)
