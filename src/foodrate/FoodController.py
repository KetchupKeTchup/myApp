"""
    __init__(main_window) - Створює FoodService, FoodUi реєструє UI у вікні (view_index), підключає btn_food i btn_add, одразу малює дашборд. Являється посередником між UI і сервісом це єдине місце де вони знають один про одного.

    show_module() - застосовується для перемикання вікон на головному екрані і оновлює данні. 

    update_dashboard() - Відповідає за підсумки дня, записує їх в чотири QLabel і прогрес бар, потім викликає update_meals_list.Його задача синхронізувати екран з БД після запуску програми і додавання новго продукту. 
    У порожньому стані lbl_calorise не скидається (рядок 42 закоментований) — після очищення даних на екрані залишиться старе число. Ще: 1000 ккал — магічна константа, її місце в config.py.

    update_meals_list() - Оновлює список з'їденої їди за сьогодні, бере дані із бд відбирає тільки ті що з сьогоднішньою датою. 

    handle_add_button() - Відкриває вікно запису продуктів при Ок бере дані, якщо None показує попередження, зберігає дані через сервіс і оновлює данні.


"""


from PyQt6.QtWidgets import QMessageBox, QHBoxLayout, QLabel
from src.foodrate.FoodService import FoodService
from src.foodrate.FoodUi import FoodUi, AddProductDialog
from datetime import datetime


class FoodController:
    def __init__(self, main_window):
        self.service = FoodService()
        self.ui = FoodUi()
        self.main_window = main_window

        # Додаємо екран у головне вікно і запам'ятовуємо його індекс
        self.view_index = self.main_window.add_module_view(self.ui)

        # Сигнали підключаємо
        self.main_window.btn_food.clicked.connect(self.show_module)
        self.ui.btn_add.clicked.connect(self.handle_add_button)

        self.update_dashboard()

    def show_module(self):
        # Перемикає головне вікно на екран харчування
        self.main_window.switch_to_view(self.view_index)
        self.update_dashboard()

    def update_dashboard(self):
        # Бере дані із бд і малює на екрані
        total_data = self.service.get_total_calories_today()

        if total_data and total_data[0] is not None and total_data[0] > 0:
            self.ui.lbl_calorise.setText(f"{total_data[1]:.0f}")
            self.ui.lbl_protein.setText(f"{total_data[2]:.0f}")
            self.ui.lbl_carbs.setText(f"{total_data[3]:.0f}")
            self.ui.lbl_fat.setText(f"{total_data[4]:.0f}")

            # Підрахунок % для прогрес бару
            progress = int((total_data[1] / 1000) * 100)
            self.ui.progress_bar.setValue(progress if progress <= 100 else 100)
        else:
            # self.ui.lbl_calories.setText("0")
            self.ui.lbl_protein.setText("0g")
            self.ui.lbl_carbs.setText("0g")
            self.ui.lbl_fat.setText("0g")
            self.ui.progress_bar.setValue(0)

        # Оновлення списку
        self.update_meals_list()

    def update_meals_list(self):
        """Створення списку з'їденого за сьогодні"""
        self.ui.clear_meals_layout()

        products = self.service.get_all_products()
        today_str = datetime.now().strftime("%Y-%m-%d")

        for p in products:
            # p = (id, назва, вага, ккал, білки, вугл, жири, дата)
            if today_str in p[7]: 
                meal_row = QHBoxLayout()
                
                lbl_name = QLabel(p[1])
                lbl_name.setStyleSheet("font-size: 14px; color: #ffffff; width: 120px;")
                
                lbl_mass = QLabel(f"• {p[2]}g")
                lbl_mass.setStyleSheet("font-size: 12px; color: #888888;")
                
                lbl_kcal = QLabel(f"• {p[3]:.0f} kcal")
                lbl_kcal.setStyleSheet("font-size: 12px; color: #ff7043;")
                
                meal_row.addWidget(lbl_name)
                meal_row.addWidget(lbl_mass)
                meal_row.addWidget(lbl_kcal)
                meal_row.addStretch()
                
                self.ui.meals_layout.addLayout(meal_row)



    def handle_add_button(self):
        """Просто відкриваємо вікно без попередніх перевірок"""
        dialog = AddProductDialog(self.ui)
        
        if dialog.exec():
            data = dialog.get_data()
            if data is None:
                QMessageBox.warning(self.ui, "Помилка", "Заповніть назву та введіть коректні числа!")
                return
                
            # Розпаковуємо 6 значень (включаючи назву)
            product_name, mass, kkal, protein, carbs, fat = data
            
            # Зберігаємо в базу
            self.service.add_product(product_name, mass, kkal, protein, carbs, fat)
            
            # Оновлюємо UI
            self.update_dashboard()