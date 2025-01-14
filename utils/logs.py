

def log_blink_count(blink_count):
    connection = sqlite3.connect("blink_counts.db")
    cursor = connection.cursor()
    
    # Insert the blink count into the table
    cursor.execute("INSERT INTO blink_logs (blink_count) VALUES (?)", (blink_count,))
    
    connection.commit()
    connection.close()


def log_blinks_periodically(self):
    # Log the current blink count to the database
    log_blink_count(self.TOTAL_BLINKS)
    
    # Schedule this function to run again after a certain interval (e.g., 5 minutes)
    self.root.after(300000, self.log_blinks_periodically)  # 300,000 ms = 5 minutes
