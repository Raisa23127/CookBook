def init_database(self):
    """Инициализация базы данных"""
    self.conn = sqlite3.connect('cookbook.db')
    cursor = self.conn.cursor()
    
    # Таблица рецептов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            cooking_time INTEGER
        )
    ''')
    
    # Таблица ингредиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT
        )
    ''')
    
    # Таблица связи рецептов и ингредиентов
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
    
    # ТАБЛИЦА СПИСКА ПОКУПОК (ДОБАВЬТЕ ЭТО)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shopping_List (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            ingredient_id INTEGER,
            quantity REAL,
            unit TEXT,
            purchased BOOLEAN DEFAULT 0,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recipe_id) REFERENCES Recipes(id),
            FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
        )
    ''')
    
    self.conn.commit()
    print("✅ База данных инициализирована")