from database.db_handler import DatabaseHandler
from datetime import date
from typing import Literal

database_handler = DatabaseHandler()
class TaskHandler():
    def add_task(self, description:str, due_date:date, priority: Literal[1,2,3]):
        database_handler.add_task_db(description, due_date, priority)

    def delete_tasks(self, ids):
        database_handler.delete_tasks_db(ids)

    def mark_task_done(self, id:int):
        database_handler.mark_task_done_db(id)

    def delete_done_tasks(self):
        tasks = database_handler.get_tasks()
        unfinished_tasks = [task['id'] for task in tasks if task['is_done'] == 1]
        self.delete_tasks(unfinished_tasks)
