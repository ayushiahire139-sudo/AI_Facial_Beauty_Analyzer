import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "database", "beauty_analyzer.db")

print("Database Path:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("\nTables Found:")

if tables:
    for table in tables:
        print(table[0])
else:
    print("No tables found.")

conn.close()