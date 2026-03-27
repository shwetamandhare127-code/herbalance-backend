import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect('herbalance.db')
cursor = conn.cursor()

# Create table with ID column
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    age INTEGER,
    weight REAL,
    bmi REAL,
    cycle_length INTEGER,
    hair_growth INTEGER,
    skin_darkening INTEGER,
    pimples INTEGER,
    weight_gain INTEGER,
    fast_food INTEGER,
    exercise INTEGER,
    prediction TEXT,
    confidence REAL,
    severity TEXT
)
''')

conn.commit()
conn.close()

print("New database created with ID column!")