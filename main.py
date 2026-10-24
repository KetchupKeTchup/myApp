import sys
from PyQt6.QtWidgets import QApplication
from src.UI.main_window import MainWindow
from src.foodrate.FoodUi import FoodUi  # Імпортуємо наш новий екран


def load_styles(style):
    """
            Download styles
            :param style:
            :return:
    """
    try:
        with open("src/UI/style.qss", "r", encoding="utf-8") as style_file:
            style_content = style_file.read()
            style.setStyleSheet(style_content)
    except FileNotFoundError:
        print("⚠️ Файл стилів style.qss не знайдено! Використовується стандартна тема.")

def main():

    
    app = QApplication(sys.argv)
    
    # 1. Створюємо оболонку
    window = MainWindow()
    
    # 2. Створюємо екран харчування
    food_screen = FoodUi()
    
    # 3. Вставляємо екран харчування в робочу зону оболонки
    window.add_module_view(food_screen)
    load_styles(app)
    
    # Показуємо все на екрані
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()