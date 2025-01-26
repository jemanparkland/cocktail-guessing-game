import sqlite3
import requests
import random

DATABASE = 'cocktails.db'
COCKTAIL_API_URL = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'

def init_db():
    """Initialize the database with a table for cocktails."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cocktails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def populate_db():
    """Add sample cocktails to the database if empty."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM cocktails')
    if cursor.fetchone()[0] == 0:
        sample_cocktails = [
            ("Margarita", "Tequila, Lime Juice, Triple Sec, Salt", "https://www.thecocktaildb.com/images/media/drink/5noda61589575158.jpg"),
            ("Mojito", "White Rum, Mint Leaves, Sugar, Lime Juice, Soda Water", "https://www.thecocktaildb.com/images/media/drink/metwgh1606770327.jpg"),
            ("Old Fashioned", "Bourbon, Sugar, Angostura Bitters, Orange Peel", "https://www.thecocktaildb.com/images/media/drink/vrwquq1478252802.jpg"),
            ("Martini", "Gin, Dry Vermouth, Olive", "https://www.thecocktaildb.com/images/media/drink/71t8581504353095.jpg"),
            ("Pina Colada", "White Rum, Coconut Cream, Pineapple Juice", "https://www.thecocktaildb.com/images/media/drink/cpf4j51504371346.jpg"),
            ("Bloody Mary", "Vodka, Tomato Juice, Lemon Juice, Worcestershire Sauce, Tabasco, Celery Salt, Black Pepper", "https://www.thecocktaildb.com/images/media/drink/t6caa21582485702.jpg"),
        ]
        cursor.executemany('INSERT INTO cocktails (name, ingredients, image_url) VALUES (?, ?, ?)', sample_cocktails)
        conn.commit()
    conn.close()

def get_random_cocktail():
    """Fetch a random cocktail from the API or fallback to the local database."""
    try:
        response = requests.get(COCKTAIL_API_URL)
        if response.status_code == 200:
            data = response.json()["drinks"][0]
            name = data["strDrink"]
            image_url = data["strDrinkThumb"]
            ingredients = []
            for i in range(1, 16):
                ingredient = data.get(f"strIngredient{i}")
                if ingredient:
                    ingredients.append(ingredient)
            return name, ingredients, image_url
    except Exception as e:
        print(f"API Error: {e}")

    # Fallback to local database if API fails
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT name, ingredients, image_url FROM cocktails ORDER BY RANDOM() LIMIT 1')
    cocktail = cursor.fetchone()
    conn.close()
    return cocktail[0], cocktail[1].split(', '), cocktail[2]
