from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QSpinBox, QPushButton,
                             QMessageBox)

class RecipeFormWindow(QDialog):
    """Окно для добавления/редактирования рецепта"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить рецепт")
        self.setGeometry(200, 200, 500, 400)
        self.initUI()
    
    def initUI(self):
        """Инициализация интерфейса формы"""
        layout = QVBoxLayout()
        
        # Поле "Название рецепта"
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название рецепта")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Поле "Описание рецепта"
        layout.addWidget(QLabel("Описание:"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Введите описание рецепта и ингредиенты...")
        layout.addWidget(self.description_input)
        
        # Поле "Время приготовления"
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Время приготовления (мин):"))
        self.time_input = QSpinBox()
        self.time_input.setRange(1, 1440)  # от 1 минуты до 24 часов
        self.time_input.setValue(30)
        time_layout.addWidget(self.time_input)
        layout.addLayout(time_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        
        self.save_button.clicked.connect(self.save_recipe)
        self.cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def get_recipe_data(self):
        """Получение данных из формы"""
        return {
            'name': self.name_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'cooking_time': self.time_input.value()
        }
    
    def save_recipe(self):
        """Сохранение рецепта"""
        data = self.get_recipe_data()
        
        # Проверка заполнения обязательных полей
        if not data['name']:
            QMessageBox.warning(self, "Ошибка", "Введите название рецепта!")
            return
        
        self.accept()  # Закрываем окно с результатом OK