import sqlite3

def log_blink_count(blink_count):
    connection = sqlite3.connect("blink_counts.db")
    cursor = connection.cursor()
    
    # Insert the blink count into the table
    cursor.execute("INSERT INTO blink_logs (blink_count) VALUES (?)", (blink_count,))
    
    connection.commit()
    connection.close()
