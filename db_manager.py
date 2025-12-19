import sqlite3
import os

# Получаем путь к базе данных относительно текущего файла
current_dir = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(current_dir, '..', 'cookbook.db')

def test_connection():
    """Тестовое подключение к базе данных"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        print("✅ Подключение к базе данных успешно установлено")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False

class DatabaseManager:
    """Класс для управления базой данных"""
    
    def __init__(self):
        self.db_name = DB_NAME
        self._create_tables()
    
    def _create_tables(self):
        """Создание необходимых таблиц в базе данных"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Создание таблицы рецептов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    cooking_time INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Создание таблицы ингредиентов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    unit TEXT
                )
            ''')
            
            # Создание таблицы связи рецептов и ингредиентов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Recipe_Ingredients (
                    recipe_id INTEGER,
                    ingredient_id INTEGER,
                    quantity REAL,
                    FOREIGN KEY (recipe_id) REFERENCES Recipes(id),
                    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id),
                    PRIMARY KEY (recipe_id, ingredient_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Таблицы успешно созданы")
        except Exception as e:
            print(f"❌ Ошибка создания таблиц: {e}")
    
    def add_recipe(self, name, description, cooking_time):
        """Добавление рецепта в базу данных"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO Recipes (name, description, cooking_time)
                VALUES (?, ?, ?)
            ''', (name, description, cooking_time))
            
            recipe_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Рецепт '{name}' добавлен с ID: {recipe_id}")
            return recipe_id
        except Exception as e:
            print(f"❌ Ошибка добавления рецепта: {e}")
            return None
    
    def get_all_recipes(self):
        """Получение всех рецептов"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name FROM Recipes ORDER BY name
            ''')
            
            recipes = cursor.fetchall()
            conn.close()
            
            print(f"✅ Получено рецептов: {len(recipes)}")
            return recipes
        except Exception as e:
            print(f"❌ Ошибка получения рецептов: {e}")
            return []
    
    def get_recipe_details(self, recipe_id):
        """Получение деталей рецепта по ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, description, cooking_time, created_at 
                FROM Recipes WHERE id = ?
            ''', (recipe_id,))
            
            recipe = cursor.fetchone()
            conn.close()
            
            if recipe:
                return {
                    'id': recipe[0],
                    'name': recipe[1],
                    'description': recipe[2],
                    'cooking_time': recipe[3],
                    'created_at': recipe[4]
                }
            return None
        except Exception as e:
            print(f"❌ Ошибка получения деталей рецепта: {e}")
            return None
    
    def get_ingredients(self, recipe_id):
        """Получение ингредиентов рецепта"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT i.name, i.unit, ri.quantity 
                FROM Ingredients i
                JOIN Recipe_Ingredients ri ON i.id = ri.ingredient_id
                WHERE ri.recipe_id = ?
            ''', (recipe_id,))
            
            ingredients = cursor.fetchall()
            conn.close()
            
            print(f"✅ Получено ингредиентов для рецепта {recipe_id}: {len(ingredients)}")
            return ingredients
        except Exception as e:
            print(f"❌ Ошибка получения ингредиентов: {e}")
            return []
    
    def update_recipe(self, recipe_id, name, description, cooking_time):
        """Обновление рецепта в базе данных"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE Recipes 
                SET name = ?, description = ?, cooking_time = ?
                WHERE id = ?
            ''', (name, description, cooking_time, recipe_id))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Рецепт с ID {recipe_id} успешно обновлен")
            return True
        except Exception as e:
            print(f"❌ Ошибка обновления рецепта: {e}")
            return False
    
    def delete_recipe(self, recipe_id):
        """Удаление рецепта из базы данных"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Сначала удаляем связанные ингредиенты
            cursor.execute('DELETE FROM Recipe_Ingredients WHERE recipe_id = ?', (recipe_id,))
            
            # Затем удаляем сам рецепт
            cursor.execute('DELETE FROM Recipes WHERE id = ?', (recipe_id,))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Рецепт с ID {recipe_id} успешно удален")
            return True
        except Exception as e:
            print(f"❌ Ошибка удаления рецепта: {e}")
            return False
    
    def search_recipes(self, search_term):
        """Поиск рецептов по названию"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name FROM Recipes 
                WHERE name LIKE ? 
                ORDER BY name
            ''', (f'%{search_term}%',))
            
            recipes = cursor.fetchall()
            conn.close()
            
            print(f"✅ Найдено рецептов по запросу '{search_term}': {len(recipes)}")
            return recipes
        except Exception as e:
            print(f"❌ Ошибка поиска рецептов: {e}")
            return []