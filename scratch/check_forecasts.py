import sqlite3
import os

def check_forecasts():
    db_path = "backend/data/forecaster.db"
    if not os.path.exists(db_path):
        db_path = "backend/backend/data/forecaster.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM forecasts;")
    count = cursor.fetchone()[0]
    print(f"Total forecasts: {count}")
    
    if count > 0:
        cursor.execute("SELECT job_id, created_at FROM forecasts ORDER BY created_at DESC LIMIT 5;")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Job ID: {row[0]}, Created: {row[1]}")
    
    conn.close()

if __name__ == "__main__":
    check_forecasts()
