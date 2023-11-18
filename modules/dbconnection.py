import sqlite3

class DBConnection:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(self.conn, *args, **kwargs)
            finally:
                #self.conn.close() # close from execute_query instead
                pass
        return wrapper

@DBConnection()
def execute_query(conn, query, data=None):
    cursor = conn.cursor()
    
    cursor.execute(query, data or []) # execute with or without {data}
    conn.commit() if data else None # commit if there is {data} (assumed INSERT)
    results = cursor.fetchall() # Empty output if using commit, safe(?) to use it here for simplicity
    cursor.close()
    return results



class insert_tbl:
    def __init__(self):
        self.db_file = 'database.db'
    def create_db(self):
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute('''CREATE TABLE IF NOT EXISTS bets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hid INTEGER,
                    position INTEGER,
                    name TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    bet INTEGER,
                    win INTEGER,
                    currency INTEGER,
                    mp INTEGER,
                    casino_name TEXT NOT NULL
                )''')
        except Exception as e:
            print(e)
