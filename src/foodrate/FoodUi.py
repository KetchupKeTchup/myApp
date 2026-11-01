
# src/foodrate/FoodUi.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QProgressBar,QDialog,QFormLayout,QDialogButtonBox, QScrollArea

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
        self._setup_macros_section(layout)
        self._setup_meals_section(layout)
        

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
        parent_layout.addSpacing(10) # 20 пікселів з низу аби відділити від наступного блоку
    
    
    def _setup_input_section(self,parent_layout):
        self.btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("+ Додати продукт")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setFixedHeight(45)
        # Зміна курсора миші на вказівний палець
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)   

        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.btn_add)
        self.btn_layout.addStretch()
        
        parent_layout.addLayout(self.btn_layout)
        parent_layout.addSpacing(5) 
    
    def _setup_meals_section(self, parent_layout):
        """Блок 3: Контейнер для списку з'їденого з можливістю прокрутки"""
        
        # Створюємо зону прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) # Вертикальна прокрутка відключенна
        self.scroll_area.setWidgetResizable(True)# Дозволяє внутрішньому контенту стискатися/розтягуватися
        self.scroll_area.setObjectName("scroll_area")# Задаємо стилі для скролбару (щоб він був темним і красивим, без білих рамок)
        self.scroll_area.setFixedHeight(350) # Фіксуємо висоту зони прокрутки, щоб вона не розтягувалась на весь екран

        #Створюємо внутрішній віджет (це буде "полотно", яке прокручується)
        self.meals_container = QWidget()
        self.meals_container.setObjectName("meals_container")
        
        # Створюємо наш старий знайомий макет і прив'язуємо його до "полотна"
        self.meals_layout = QVBoxLayout(self.meals_container)
        self.meals_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Притискаємо всі продукти догори
        self.meals_layout.setSpacing(10) # Відстань між продуктами

        #  Кладемо "полотно" всередину зони прокрутки
        self.scroll_area.setWidget(self.meals_container)

        #  Додаємо зону прокрутки на головний екран
        parent_layout.addWidget(self.scroll_area)
        parent_layout.addSpacing(10)
    
    def _setup_macros_section(self, parent_layout):
        # Блок 4: Відображення макронутрієнтів (білки, вуглеводи, жири)
        self.macros_style = QWidget()
        self.macros_style.setObjectName("macros_style")
        self.macros_style.setContentsMargins(0, 15, 0, 15) # Встановлює відстані між краями padding не працює в стилях QSS,тому використовується setContentsMargins
        
        self.macros_layout = QHBoxLayout(self.macros_style)
        
        self.lbl_protein = self._create_macro_widget("Білки", "0", self.macros_layout)
        self.lbl_carbs = self._create_macro_widget("Вуглеводи", "0", self.macros_layout)
        self.lbl_fat = self._create_macro_widget("Жири", "0", self.macros_layout)

        parent_layout.addWidget(self.macros_style)

    def _create_macro_widget(self, name, default_value, parent_layout):
        # Створює віджет для макронутрієнта (назва + значення) і додає його в батьківський макет
        m_layout = QHBoxLayout()
        
        m_container = QWidget()
        m_container.setObjectName("macro_conteiner")
        m_container.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) # Дозволяє стилізувати фон віджета через QSS

        m_container_layout = QVBoxLayout(m_container)

        m_name = QLabel(name)
        m_name.setProperty("cssClass", "macro_name") # Використовується для додавання 
                                                     # стилів групи однакових елементів setObjectName використовується як id і для кожного елемента потрібний унікальний

        m_val = QLabel(default_value)
        m_val.setProperty("cssClass", "macro_val")

        m_container_layout.addWidget(m_name, alignment=Qt.AlignmentFlag.AlignCenter)
        m_container_layout.addWidget(m_val, alignment=Qt.AlignmentFlag.AlignCenter)

        m_layout.addWidget(m_container)
        parent_layout.addLayout(m_layout)
        return m_val

    def clear_meals_layout(self):
            """Очищує список продуктів перед його оновлення, щоб не було дублікатів"""
            while self.meals_layout.count():
                child = self.meals_layout.takeAt(0) 
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    while child.layout().count():
                        sub_child = child.layout().takeAt(0)
                        if sub_child.widget():
                            sub_child.widget().deleteLater()
                    child.layout().deleteLater()

class AddProductDialog(QDialog):
    # Діалогове вікно для додавання нового продукту

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додати новий продукт")
        self.setObjectName("dialog_title")

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Поле для назви продукта-страви
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Молоко")

        # Поля для цифр
        self.mass_input = QLineEdit("")
        self.kkal_input = QLineEdit("")
        self.prot_input = QLineEdit("")
        self.carbs_input = QLineEdit("")
        self.fat_input = QLineEdit("")

        # прописуємо стилі всім полям одночасно
        for inp in [self.mass_input, self.kkal_input, self.prot_input, self.carbs_input, self.fat_input]:
            inp.setObjectName("input_style")

        form_layout.addRow("Назва продукту:", self.name_input)
        form_layout.addRow("Вага (г):", self.mass_input)
        form_layout.addRow("Ккал на 100г:", self.kkal_input)
        form_layout.addRow("Білки на 100г:", self.prot_input)
        form_layout.addRow("Вуглеводи на 100г:", self.carbs_input)
        form_layout.addRow("Жири на 100г:", self.fat_input)

        layout.addLayout(form_layout)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_data(self):
        # Збирає всі дані з полів і повертає їх у вигляді кортежу, або None якщо дані некоректні
        try:
            name = self.name_input.text().strip()
            if not name:
                return None
            return(
                name,
                float(self.mass_input.text()),
                float(self.kkal_input.text()),
                float(self.prot_input.text()),
                float(self.carbs_input.text()),
                float(self.fat_input.text())
            )
        except ValueError:
            return None


    








