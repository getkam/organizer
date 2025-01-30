import sqlite3
from datetime import date
from config import DATABASE_PATH
from typing import Literal

class DatabaseHandler():
    
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        


    def get_conn(self): 
        '''Creating connection fo database'''
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def add_task_db(self, description: str, due_date: date = date.today(), priority: Literal[1,2,3] = 2): 
        '''Add new task to database'''
        with self.get_conn() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                        INSERT INTO tasks(description, due_date, priority, is_done) VALUES(?,?,?,?)
                        ''',
                        (description, due_date, priority, 0)
                        )
            connection.commit()

    def get_tasks(self):
        '''Retrieving all tasks from data base'''
        with self.get_conn() as connection:
            cursor = connection.cursor();
            cursor.execute('''
                            SELECT id, description, due_date, priority, is_done FROM tasks
                        ''')
            return cursor.fetchall()

    def delete_tasks_db(self, task_ids):
        '''Deleting tasks from database'''
        if not task_ids:
            #print("No task to delete")
            return
        placeholders = ', '.join('?' for _ in task_ids)
        with self.get_conn() as connection:
            cursor = connection.cursor()
            cursor.execute(f'''
                            DELETE FROM tasks WHERE id IN ({placeholders})
                            ''',task_ids)
            connection.commit()

    def mark_task_done_db(self, id: int):
        '''Updating column "Done" for provided task id'''
        with self.get_conn() as connection:
            cursor = connection.cursor()
            if self.id_exist(id):
                cursor.execute('''
                            UPDATE tasks
                            SET is_done = 1
                            WHERE id = ? 
                            ''', [str(id)])
            else: 
                raise ValueError(f"Task with id {id} doesn't exist")
            connection.commit()
    
    def id_exist(self, id:int) -> bool:
        '''Checking if provided id existing in database'''
        with self.get_conn() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM tasks WHERE id = ?", [id])
            return len(cursor.fetchall()) == 1 