"""
    __init__(main_window) - Створює FoodService, FoodUi реєструє UI у вікні (view_index), підключає btn_food i btn_add, одразу малює дашборд. Являється посередником між UI і сервісом це єдине місце де вони знають один про одного.

    show_module() - застосовується для перемикання вікон на головному екрані і оновлює данні. 

    update_dashboard() - Відповідає за підсумки дня, записує їх в чотири QLabel і прогрес бар, потім викликає update_meals_list.Його задача синхронізувати екран з БД після запуску програми і додавання новго продукту. 
    У порожньому стані lbl_calorise не скидається (рядок 42 закоментований) — після очищення даних на екрані залишиться старе число. Ще: 1000 ккал — магічна константа, її місце в config.py.

    update_meals_list() - Оновлює список з'їденої їди за сьогодні, бере дані із бд відбирає тільки ті що з сьогоднішньою датою. 

    handle_add_button() - Відкриває вікно запису продуктів при Ок бере дані, якщо None показує попередження, зберігає дані через сервіс і оновлює данні.


"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem,QMenu
from src.foodrate.FoodService import FoodService
from src.foodrate.FoodUi import FoodUi, AddProductDialog, EditProductDialog
from datetime import datetime, timedelta


class FoodController:
    def __init__(self, main_window):
        self.service = FoodService()
        self.ui = FoodUi()
        self.main_window = main_window

        #-------------- filter -----------------------
        # Стандартне значення фільтра
        self.current_filter = "today"
        self.ui.btn_today.clicked.connect(self.set_filter_today)
        self.ui.btn_week.clicked.connect(self.set_filter_week)

        # Додаємо екран у головне вікно і запам'ятовуємо його індекс
        self.view_index = self.main_window.add_module_view(self.ui)

        # ------------------ Сигнали ----------------------
        self.main_window.btn_food.clicked.connect(self.show_module)
        self.ui.btn_add.clicked.connect(self.handle_add_button) # Сигнал для кнопки додати продукт
        
        # Сигнал для контекстного меню таблиці
        self.ui.meals_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.meals_table.customContextMenuRequested.connect(self.show_context_menu)
        

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
        """Заповнення таблиці продуктів"""
        self.ui.meals_table.setRowCount(0)  # Очищуємо таблицю

        products = self.service.get_all_products()

        # Вираховуємо дату
        now = datetime.now()
        today_str = datetime.now().strftime("%Y-%m-%d")
        week_ago = now - timedelta(days=7)

        show_record = False
        
        row_index = 0 # Індекс рядка для таблиці
        
        for p in products:
            record_date_str = str(p[7])

            if self.current_filter == "today":
                if today_str in record_date_str:
                    show_record = True
            elif self.current_filter == "week":
                try:
                    # Обрізаємо перші 10 символів (YYYY-MM-DD), щоб порівняти дати
                    record_date = datetime.strptime(record_date_str[:10], "%Y-%m-%d")
                    # Якщо дата запису лежить між (сьогодні - 7 днів) та сьогодні
                    if week_ago.date() <= record_date.date() <= now.date():
                        show_record = True
                except ValueError:
                    pass

            if show_record:
                name_item = QTableWidgetItem(str(p[1]))
                name_item.setData(Qt.ItemDataRole.UserRole, p[0])
                
                self.ui.meals_table.insertRow(row_index)
                
                self.ui.meals_table.setItem(row_index, 0, name_item)  
                self.ui.meals_table.setItem(row_index, 1, QTableWidgetItem(f"{p[2]}g"))  
                self.ui.meals_table.setItem(row_index, 2, QTableWidgetItem(f"{p[3]:.0f} kcal"))  
                self.ui.meals_table.setItem(row_index, 3, QTableWidgetItem(f"{p[4]}g"))  
                self.ui.meals_table.setItem(row_index, 4, QTableWidgetItem(f"{p[5]}g"))  
                self.ui.meals_table.setItem(row_index, 5, QTableWidgetItem(f"{p[6]}g"))  
                
                row_index += 1

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

    def show_context_menu(self, position):
        """Відкриває контекстне меню при натисканні правої кнопки миші на таблиці"""

       # Отримання індексу рядка, на якому було натиснуто
        row_table = self.ui.meals_table.rowAt(position.y())
        
        if row_table < 0:
            return

        # Виділяємо весь рядок
        self.ui.meals_table.selectRow(row_table)

        # Створення меню 
        menu = QMenu()

        full_info = menu.addAction("Повна інформація")
        edit_action = menu.addAction("Редагувати")
        delete_action = menu.addAction("Видалити")

        # Показати меню там де знаходиться курсор миші
        action = menu.exec(self.ui.meals_table.viewport().mapToGlobal(position))

        if action == full_info:
            self.full_info(row_table)
        if action == edit_action:
            self.edit_action(row_table)
        if action == delete_action:
            self.delete_record(row_table)

    def edit_action(self, row_table):
        """Редагування записаного продукту"""
        table_id_item = self.ui.meals_table.item(row_table, 0)
        dialog_window = EditProductDialog(self.ui)
        dialog_window.exec()# відкриття вікна
        

    def delete_record(self, row_table):
        """Видалення запису"""
        table_id_item = self.ui.meals_table.item(row_table, 0)

        
        if not table_id_item:
            QMessageBox.warning("Помилка", "Невдалось видалити запис")
            return 

        # Отримання реального ID із бази 
        real_id_record = table_id_item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self.ui, "Видалення", f"Видалити?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete_product(real_id_record)
            self.update_dashboard()

    def full_info(self, row_table):
        rrr = row_table
        QMessageBox.about(self.ui, "", f"В розробці")

    def set_filter_today(self):
        self.current_filter = 'today'
        self.update_meals_list()

    def set_filter_week(self):
        self.current_filter = 'week'
        self.update_meals_list()
        