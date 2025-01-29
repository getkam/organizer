import sqlite3

def init_db(database_path = "organizer.db"): 
  '''
  Creates database and tables if they are not existing
  
  '''
  with sqlite3.connect(database_path) as connection: 
    cursor = connection.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   description TEXT NOT NULL, 
                   due_date DATE,
                   is_done BOOLEAN NOT NULL DEFAULT 0
                   )
                   """)
    connection.commit()

if __name__=='__main__':
  init_db()
