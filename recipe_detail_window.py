from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QLineEdit, QSpinBox,
                             QMessageBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt

class RecipeDetailWindow(QDialog):
    """Окно для просмотра и редактирования деталей рецепта"""
    
    def __init__(self, recipe_data, db_manager, parent=None):
        super().__init__(parent)
        self.recipe_data = recipe_data
        self.db_manager = db_manager
        self.is_editing = False
        self.setWindowTitle(f"Рецепт: {recipe_data['name']}")
        self.setGeometry(300, 300, 600, 500)
        self.initUI()
    
    def initUI(self):
        """Инициализация интерфейса деталей рецепта"""
        layout = QVBoxLayout()
        
        # Название рецепта (редактируемое)
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit(self.recipe_data['name'])
        self.name_input.setReadOnly(True)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Время приготовления (редактируемое)
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Время приготовления (мин):"))
        self.time_input = QSpinBox()
        self.time_input.setRange(1, 1440)
        self.time_input.setValue(self.recipe_data['cooking_time'])
        self.time_input.setReadOnly(True)
        time_layout.addWidget(self.time_input)
        layout.addLayout(time_layout)
        
        # Описание рецепта (редактируемое)
        layout.addWidget(QLabel("Описание и ингредиенты:"))
        self.description_input = QTextEdit()
        self.description_input.setPlainText(self.recipe_data['description'])
        self.description_input.setReadOnly(True)
        layout.addWidget(self.description_input)
        
        # Список ингредиентов
        layout.addWidget(QLabel("Ингредиенты:"))
        self.ingredients_label = QLabel("Загрузка ингредиентов...")
        layout.addWidget(self.ingredients_label)
        self.load_ingredients()
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        self.close_button = QPushButton("Закрыть")
        
        self.edit_button.clicked.connect(self.toggle_edit)
        self.delete_button.clicked.connect(self.delete_recipe)
        self.close_button.clicked.connect(self.accept)
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.close_button)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def load_ingredients(self):
        """Загрузка ингредиентов рецепта"""
        try:
            ingredients = self.db_manager.get_ingredients(self.recipe_data['id'])
            if ingredients:
                ingredients_text = ""
                for name, unit, quantity in ingredients:
                    if unit and quantity:
                        ingredients_text += f"• {name}: {quantity} {unit}\n"
                    else:
                        ingredients_text += f"• {name}\n"
                self.ingredients_label.setText(ingredients_text)
            else:
                self.ingredients_label.setText("Ингредиенты не указаны")
        except Exception as e:
            print(f"❌ Ошибка загрузки ингредиентов: {e}")
            self.ingredients_label.setText("Ошибка загрузки ингредиентов")
    
    def toggle_edit(self):
        """Переключение режима редактирования"""
        if not self.is_editing:
            # Включаем редактирование
            self.name_input.setReadOnly(False)
            self.time_input.setReadOnly(False)
            self.description_input.setReadOnly(False)
            self.edit_button.setText("Сохранить")
            self.is_editing = True
        else:
            # Сохраняем изменения
            self.save_changes()
    
    def save_changes(self):
        """Сохранение изменений рецепта"""
        try:
            new_name = self.name_input.text().strip()
            new_description = self.description_input.toPlainText().strip()
            new_time = self.time_input.value()
            
            if not new_name:
                QMessageBox.warning(self, "Ошибка", "Название рецепта не может быть пустым!")
                return
            
            # Обновляем в базе данных
            success = self.db_manager.update_recipe(
                self.recipe_data['id'],
                new_name,
                new_description,
                new_time
            )
            
            if success:
                # Обновляем данные
                self.recipe_data['name'] = new_name
                self.recipe_data['description'] = new_description
                self.recipe_data['cooking_time'] = new_time
                
                # Возвращаем в режим просмотра
                self.name_input.setReadOnly(True)
                self.time_input.setReadOnly(True)
                self.description_input.setReadOnly(True)
                self.edit_button.setText("Редактировать")
                self.is_editing = False
                self.setWindowTitle(f"Рецепт: {new_name}")
                
                QMessageBox.information(self, "Успех", "Рецепт успешно обновлен!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить рецепт!")
                
        except Exception as e:
            print(f"❌ Ошибка сохранения изменений: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить изменения: {e}")
    
    def delete_recipe(self):
        """Удаление рецепта"""
        reply = QMessageBox.question(
            self, 
            "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить рецепт '{self.recipe_data['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.db_manager.delete_recipe(self.recipe_data['id'])
                if success:
                    QMessageBox.information(self, "Успех", "Рецепт успешно удален!")
                    self.accept()  # Закрываем окно
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить рецепт!")
            except Exception as e:
                print(f"❌ Ошибка удаления рецепта: {e}")
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить рецепт: {e}")