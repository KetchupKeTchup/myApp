# src/foodrate/FoodUi.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QProgressBar
from PyQt6.QtCore import Qt

class FoodUi(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Викликаємо методи, які малюють окремі блоки
        self._setup_calories_section(layout)
        self._setup_input_section(layout)
        self._setup_meals_section(layout)
        self._setup_macros_section(layout)

        layout.addStretch()  # Додаємо розтягування, щоб блоки були зверху


    def _setup_calories_section(self, parent_layout):
        # Створення віджетта тексту QLabel для відображення калорй
        # Використовується self для того щоб в подальшому можна було до нього звернутись і міняти значення
        self.lbl_calorise = QLabel("0")
        
        # Прив'язка ID до цього елемента для стилів
        self.lbl_calorise.setObjectName("calories_main")
        
        # Вирівнюємо текст рівно по центру
        self.lbl_calorise.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Просто текст для калорій
        # self не використовується, томущо це просто текст в цьому випадку і змінюватись він не буде
        lbl_subtitle = QLabel("Kcal")
        lbl_subtitle.setObjectName("calories_progress")
        lbl_subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Полоска прогресу(self для того щоб звиртатись і змінювати параметри)
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("calories_progress")
        self.progress_bar.setFixedHeight(4) # Просто фіксуємо висоту в 4 пікселі
        self.progress_bar.setTextVisible(False) # Приховуємо текст відсотків, типово QProgressBar пише "0%"
        self.progress_bar.setValue(0) # Стартове значення 0

        # Почергі складаємо всі віджети
        parent_layout.addWidget(self.lbl_calorise)
        parent_layout.addWidget(lbl_subtitle)
        parent_layout.addWidget(self.progress_bar)
        parent_layout.addSpacing(20) # 20 пікселів з низу аби відділити від наступного блоку
    
    
    def _setup_input_section(self,parent_layout):
        self.search_layout = QHBoxLayout()

        self.input_food = QLineEdit()
        self.input_food.setObjectName("food_input")
        self.input_food.setPlaceholderText("Вкажіть назву продукту: ")
        self.input_food.setFixedHeight(45)

        self.btn_add = QPushButton("+")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setFixedSize(45,45)
        # Зміна курсора миші на вказівний палець
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)   

        self.search_layout.addWidget(self.input_food)
        self.search_layout.addWidget(self.btn_add)
        parent_layout.addLayout(self.search_layout)
        parent_layout.addSpacing(20) 
    
    def _setup_meals_section(self, parent_layout):
        self.meals_layout = QHBoxLayout()
        parent_layout.addLayout(self.meals_layout)
        parent_layout.addSpacing(20)



        
    def _setup_macros_section(self, parent_layout):
        self.macros_layout = QHBoxLayout()

        self.lbl_protein = self._create_macro_widget("Білки", "0", self.macros_layout)
        self.lbl_carbs = self._create_macro_widget("Вуглеводи", "0", self.macros_layout)
        self.lbl_fat = self._create_macro_widget("Жири", "0", self.macros_layout)

        parent_layout.addLayout(self.macros_layout)


    def _create_macro_widget(self, name, default_value, parent_layout):
        m_layout = QVBoxLayout()

        m_name = QLabel(name)
        m_name.setProperty("cssClass", "macro_name") # Використовується для додавання 
                                                     # стилів групи однакових елементів setObjectName використовується як id і для кожного елемента потрібний унікальний

        m_val = QLabel(default_value)
        m_val.setProperty("cssClass", "macro_val")

        m_layout.addWidget(m_name, alignment=Qt.AlignmentFlag.AlignHCenter)
        m_layout.addWidget(m_val, alignment=Qt.AlignmentFlag.AlignHCenter)
        parent_layout.addLayout(m_layout)
        return m_val







