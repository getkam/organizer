import sqlite3
from datetime import date
from config import DATABASE_PATH
from typing import Literal
from models.task import Task

class DatabaseHandler():
    
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        
    def get_conn(self): 
        '''Creating connection fo database'''
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def add_task_db(self, task: Task): 
        '''Add new task to database'''
        with self.get_conn() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                        INSERT INTO tasks(description, due_date, priority, is_done) VALUES(?,?,?,?)
                        ''',
                        (task.description, task.due_date, task.priority, task.is_done)
                        )
            connection.commit()

    def get_task_by_id(self, id:int) -> Task:
        '''Retrieving one record fr if provided id existing in database'''
        with self.get_conn() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, description, due_date, priority, is_done FROM tasks WHERE id = ?", [id])
            row = cursor.fetchone()
            if row:
                return Task(
                    task_id = row['id'], 
                    description = row['description'], 
                    due_date = row['due_date'],
                    priority = row['priority'], 
                    is_done = row['is_done']
                )
            else:
                raise ValueError(f"Task with id {id} doesn't exist")
        
    def get_tasks(self)->list[Task]:
        '''Retrieving all tasks from data base'''
        with self.get_conn() as connection:
            cursor = connection.cursor();
            cursor.execute('''
                            SELECT id, description, due_date, priority, is_done FROM tasks
                        ''')
            rows = cursor.fetchall()
            return [Task (
                task_id = row['id'], 
                    description = row['description'], 
                    due_date = row['due_date'],
                    priority = row['priority'], 
                    is_done = row['is_done']
            ) for row in rows]

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