import sys
import logging
from utils.loger_config import setup_logging
from PyQt6.QtWidgets import QApplication
from src.UI.main_window import MainWindow
from src.foodrate.FoodController import FoodController
"""
    main() - Це єдина точка входу, яка збирає всі шари до єдиного купи. 
    Тут створюється QApplication(sys.argv) це фундамент графічної програми, він діє як двигун.
"""

setup_logging()
loger = logging.getLogger(__name__)

def main():
    app = QApplication(sys.argv)
    
    # Підключаємо стилі
    try:
        with open("src/UI/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Помилка: style.qss не знайдено!")
    
    # 1. Створюємо оболонку
    window = MainWindow()
    
    # 2. Створюємо контролер (він сам створить FoodUi і вставить його у вікно)
    food_controller = FoodController(window)
    
    # 3. Показуємо екран харчування першим
    window.switch_to_view(food_controller.view_index)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()