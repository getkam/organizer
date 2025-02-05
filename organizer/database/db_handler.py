import sqlite3
from organizer.models.task import Task


DATABASE_PATH = "database/organizer.db"
class DatabaseHandler():
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.connection.row_factory = sqlite3.Row
    
    def close_connection(self):
        '''Closing connection to database'''
        self.connection.close

    def add_task(self, task: Task): 
        '''Add new task to database'''
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute('''
                        INSERT INTO tasks(description, due_date, priority, is_done) VALUES(?,?,?,?)
                        ''',
                        (task.description, task.due_date, task.priority, task.is_done)
                        )
            connection.commit()

    def get_task_by_id(self, id:int) -> Task:
        '''Retrieving one record fr if provided id existing in database'''
        with self.connection as connection:
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
        with self.connection as connection:
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

    def delete_tasks(self, task_ids):
        '''Deleting tasks from database'''
        if not task_ids:
            raise ValueError("Provide tasks to delete")
        placeholders = ', '.join('?' for _ in task_ids)
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute(f'''
                            DELETE FROM tasks WHERE id IN ({placeholders})
                            ''',task_ids)
            connection.commit()

    def mark_task_done(self, id: int):
        '''Updating column "Done" for provided task id'''
        with self.connection as connection:
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
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM tasks WHERE id = ?", [id])
            return len(cursor.fetchall()) == 1 