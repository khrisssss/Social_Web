import sqlite3
import os 


DB_NAME = "./database/data_cousadobo.db"
def get_Connection():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_Users_Table():
    conn = get_Connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS USER(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT UNIQUE NOT NULL,
        profil_photo TEXT,
        score FLOAT, 
        implication_score FLOAT, 
        mot_de_pass TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

get_Connection()
create_Users_Table()