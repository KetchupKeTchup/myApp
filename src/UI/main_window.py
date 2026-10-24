# src/UI/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QStackedWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AnFin - Головне вікно")
        self.setGeometry(100, 100, 1000, 700)
        
        # Встановлюємо загальний темний фон для вікна
        self.setStyleSheet("background-color: #121212; color: white;")

        # 1. Головний віджет, який займає все вікно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 2. Головний макет
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 3. Викликаємо функції для створення лівої і правої частин
        self._setup_sidebar()
        self._setup_workspace()

    def _setup_sidebar(self):
        """Створює ліве бокове меню"""
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(70)
        self.sidebar.setStyleSheet("background-color: #1a1a1a; border-right: 1px solid #2a2a2a;")
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        
        # Кнопка Харчування
        self.btn_food = QPushButton("🍴")
        self.btn_food.setFixedSize(50, 50)
        self.btn_food.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_food.setStyleSheet("""
            background: transparent; 
            border: none; 
            font-size: 24px; 
            color: #ff7043; 
            border-left: 3px solid #ff7043;
        """)

        sidebar_layout.addWidget(self.btn_food, alignment=Qt.AlignmentFlag.AlignHCenter)
        sidebar_layout.addStretch() 
        
        self.main_layout.addWidget(self.sidebar)

    def _setup_workspace(self):
        """Створює праву робочу зону (стек екранів)"""
        self.workspace = QStackedWidget()
        self.main_layout.addWidget(self.workspace)

    def add_module_view(self, widget):
        """Додає новий екран у робочу зону"""
        return self.workspace.addWidget(widget)

    def switch_to_view(self, index):
        """Перемикає видимий екран"""
        self.workspace.setCurrentIndex(index)