import sqlite3

def initialize_database():
    connection = sqlite3.connect("blink_counts.db")
    cursor = connection.cursor()
    
    # Create a table to store blink counts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blink_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            blink_count INTEGER
        )
    """)
    
    connection.commit()
    connection.close()
