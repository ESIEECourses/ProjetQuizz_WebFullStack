import sqlite3
from pathlib import Path

def create_database():
    try:
        conn = sqlite3.connect(Path(__file__).parent.resolve() / 'QuizDB.db')
        cursor = conn.cursor()

        # DELETE OLD TABLES
        cursor.execute('DROP TABLE IF EXISTS question')
        cursor.execute('DROP TABLE IF EXISTS answer')
        cursor.execute('DROP TABLE IF EXISTS player')
        
        
        # CREATE TABLES
        cursor.execute('''CREATE TABLE "Answer" (
                        "id"	INTEGER,
                        "value"	TEXT NOT NULL,
                        "correct"	INTEGER NOT NULL DEFAULT 0,
                        "questionID"	INTEGER NOT NULL,
                        FOREIGN KEY("questionID") REFERENCES "Question"("id"),
                        PRIMARY KEY("id")
                        )''')
        
        cursor.execute('''CREATE TABLE "Player" (
                            "id"	INTEGER,
                            "name"	TEXT NOT NULL UNIQUE,
                            "score"	INTEGER DEFAULT 0,
                            PRIMARY KEY("id")
                        )''')
        
        cursor.execute('''CREATE TABLE "Question" (
                            "id"	INTEGER,
                            "title"	TEXT NOT NULL,
                            "text"	TEXT NOT NULL,
                            "img"	TEXT NOT NULL,
                            "pos"	INTEGER NOT NULL UNIQUE,
                            PRIMARY KEY("id")
                        )''')
             
        conn.commit()
        return 'Ok', 200

    except Exception as err:
        print(err)
        return 'Error', 404