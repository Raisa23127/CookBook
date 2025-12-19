from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt

class ShoppingListWindow(QDialog):
    """Окно для просмотра списка покупок"""
    
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.setWindowTitle("🛒 Список покупок")
        self.setGeometry(400, 200, 700, 500)
        
        self.initUI()
        self.load_shopping_list()
    
    def initUI(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("🛒 Мой список покупок")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Таблица списка покупок
        self.shopping_table = QTableWidget()
        self.shopping_table.setColumnCount(5)
        self.shopping_table.setHorizontalHeaderLabels(["Куплено", "Ингредиент", "Количество", "Рецепт", "Действия"])
        self.shopping_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.shopping_table.setColumnWidth(0, 80)
        self.shopping_table.setColumnWidth(2, 100)
        self.shopping_table.setColumnWidth(3, 150)
        self.shopping_table.setColumnWidth(4, 80)
        layout.addWidget(self.shopping_table)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("🧹 Очистить список")
        self.clear_button.clicked.connect(self.clear_shopping_list)
        
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.accept)
        
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.close_button)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def load_shopping_list(self):
        """Загрузка списка покупок"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT sl.id, i.name, sl.quantity, sl.unit, r.name, sl.purchased
            FROM Shopping_List sl
            JOIN Ingredients i ON sl.ingredient_id = i.id
            JOIN Recipes r ON sl.recipe_id = r.id
            ORDER BY sl.purchased, i.name
        ''')
        
        items = cursor.fetchall()
        self.shopping_table.setRowCount(len(items))
        
        for row, (item_id, ingredient_name, quantity, unit, recipe_name, purchased) in enumerate(items):
            # CheckBox для отметки о покупке
            checkbox = QCheckBox()
            checkbox.setChecked(bool(purchased))
            checkbox.stateChanged.connect(lambda state, item_id=item_id: self.toggle_purchased(item_id, state))
            self.shopping_table.setCellWidget(row, 0, checkbox)
            
            # Ингредиент
            self.shopping_table.setItem(row, 1, QTableWidgetItem(ingredient_name))
            
            # Количество
            quantity_text = f"{quantity} {unit}" if unit != "по вкусу" else unit
            self.shopping_table.setItem(row, 2, QTableWidgetItem(quantity_text))
            
            # Рецепт
            self.shopping_table.setItem(row, 3, QTableWidgetItem(recipe_name))
            
            # Кнопка удаления
            delete_button = QPushButton("🗑️")
            delete_button.clicked.connect(lambda checked, item_id=item_id: self.delete_item(item_id))
            self.shopping_table.setCellWidget(row, 4, delete_button)
            
            # Визуальное выделение купленных items
            if purchased:
                for col in range(5):
                    item = self.shopping_table.item(row, col)
                    if item:
                        item.setBackground(Qt.GlobalColor.lightGray)
    
    def toggle_purchased(self, item_id, state):
        """Переключение статуса покупки"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE Shopping_List SET purchased = ? WHERE id = ?
        ''', (1 if state == 2 else 0, item_id))
        self.conn.commit()
        
        # Обновляем отображение
        self.load_shopping_list()
    
    def delete_item(self, item_id):
        """Удаление item из списка покупок"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM Shopping_List WHERE id = ?', (item_id,))
        self.conn.commit()
        
        self.load_shopping_list()
        QMessageBox.information(self, "Успех", "Позиция удалена из списка покупок!")
    
    def clear_shopping_list(self):
        """Очистка всего списка покупок"""
        reply = QMessageBox.question(
            self, 
            "Подтверждение очистки", 
            "Вы уверены, что хотите очистить весь список покупок?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM Shopping_List')
            self.conn.commit()
            
            self.load_shopping_list()
            QMessageBox.information(self, "Успех", "Список покупок очищен!")