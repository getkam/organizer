import sqlite3
from datetime import date


DATABASE_PATH = "database/organizer.db"

def get_conn(): 
    '''Creating connection fo database'''
    return sqlite3.connect(DATABASE_PATH)

def add_task_db(description: str, due_date = date.today()): 
    '''Add new task to database'''
    with get_conn() as connection:
        cursor = connection.cursor()
        cursor.execute('''
                       INSERT INTO tasks(description, due_date, is_done) VALUES(?,?,?)
                       ''',
                       (description, due_date, 0,)
                       )
        connection.commit()

def get_tasks():
    '''Retriving all tasks from data base'''
    with get_conn() as connection:
        cursor = connection.cursor();
        cursor.execute('''
                        SELECT * FROM tasks
                       ''')
        return cursor.fetchall()

def delete_tasks_db(task_ids):
    '''Deleting tasks from database'''
    if not task_ids:
        #print("No task to delete")
        return
    placeholders = ', '.join('?' for _ in task_ids)
    with get_conn() as connection:
        cursor = connection.cursor()
        cursor.execute(f'''
                      DELETE FROM tasks WHERE id IN ({placeholders})
                      ''',task_ids)
        connection.commit()

def mark_task_done_db(id: int):
    '''Updating column "Done" for provided task id'''
    with get_conn() as connection:
        cursor = connection.cursor()
        cursor.execute('''
                       UPDATE tasks
                       SET is_done = 1
                       WHERE id = ? 
                       ''', [str(id)])
        connection.commit()