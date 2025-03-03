import sqlite3
import os

def create_sqlite_db():
    # Create SQLite database if it doesn't exist
    root_path = os.getenv("ROOTPATH")
    db_path = root_path + "/hiring_helper.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create job descriptions table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_descriptions (
            job_description_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_description TEXT NOT NULL,
            canonical_job_description TEXT NOT NULL,
            job_title TEXT NOT NULL
        )
    ''')


    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_sqlite_db()