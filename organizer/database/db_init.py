import sqlite3


DATABASE_PATH = "database/organizer.db"

def init_db(database_path = DATABASE_PATH): 
  '''
  Creates database and tables if they are not existing
  
  '''
  with sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES) as connection: 
    cursor = connection.cursor()
    cursor.execute("""
                  CREATE TABLE IF NOT EXISTS tasks(
                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  description TEXT NOT NULL, 
                  due_date DATE NOT NULL,
                  priority INTEGER CHECK(priority IN (1, 2, 3)) DEFAULT 2,
                  is_done BOOLEAN NOT NULL DEFAULT 0
                  )
                  """)
    connection.commit()


if __name__=='__main__':
  init_db()
