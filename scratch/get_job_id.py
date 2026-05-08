import sqlite3
import os

def get_job_id():
    db_path = "backend/data/forecaster.db"
    if not os.path.exists(db_path):
        db_path = "backend/backend/data/forecaster.db"
    
    if not os.path.exists(db_path):
        print("Database not found.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT job_id FROM jobs ORDER BY created_at DESC LIMIT 1;")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        print(f"Found Job ID: {row[0]}")
    else:
        print("No jobs found in database.")

if __name__ == "__main__":
    get_job_id()
