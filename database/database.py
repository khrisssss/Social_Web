import sqlite3
import os

DB_NAME = "./database/data_cousadobo.db"


#Connexion
def get_connection():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

# activer les foreign keys dans SQLite
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

#USER
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT UNIQUE NOT NULL,
        mot_de_passe TEXT NOT NULL,
        profil_photo TEXT,
        score REAL DEFAULT 0,
        implication_score REAL DEFAULT 0
    )
    """)

#MESSAGE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS message (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creator_id INTEGER NOT NULL,
        content TEXT,
        image TEXT,
        FOREIGN KEY (creator_id) REFERENCES user(id) ON DELETE CASCADE
    )
    """)

#RESPONSE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS response (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE,
        FOREIGN KEY (creator_id) REFERENCES user(id) ON DELETE CASCADE
    )
    """)

#TAGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

#FOLLOWERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS follower (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        follower_id INTEGER NOT NULL,
        following_id INTEGER NOT NULL,
        FOREIGN KEY (follower_id) REFERENCES user(id) ON DELETE CASCADE,
        FOREIGN KEY (following_id) REFERENCES user(id) ON DELETE CASCADE,
        UNIQUE(follower_id, following_id)
    )
    """)

#MESSAGE_TAG
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS message_tag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE,
        UNIQUE(message_id, tag_id)
    )
    """)

#INTERESSES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interesse (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
        UNIQUE(message_id, user_id)
    )
    """)

#DESINTERESSES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS desinteresse (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
        UNIQUE(message_id, user_id)
    )
    """)

#LIKES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS like (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
        UNIQUE(message_id, user_id)
    )
    """)

# DISLIKES 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dislike (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
        UNIQUE(message_id, user_id)
    )
    """)

    conn.commit()
    conn.close()


# Initiation de la DB

if __name__ == "__main__":
    create_tables()
    print("Database créée avec succès.")