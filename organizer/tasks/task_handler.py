from datetime import date
from typing import Literal

from organizer.database.db_handler import DatabaseHandler
from organizer.models.task import Task

class TaskHandler():
    def __init__(self, database_handler:DatabaseHandler):
        self.database_handler = database_handler

    def add_task(self, description:str, due_date:date = date.today(), priority: Literal[1,2,3] = 2):
        self.database_handler.add_task(Task(description=description, due_date=due_date, priority=priority, is_done = False))

    def delete_tasks(self, ids:list[int]):
        self.database_handler.delete_tasks(ids)

    def mark_task_done(self, task:Task):
        if task.task_id:
            self.database_handler.mark_task_done(task.task_id)

    def delete_done_tasks(self):
        tasks = self.database_handler.get_tasks()
        unfinished_tasks = [task.task_id for task in tasks if task.is_done == 1]
        self.delete_tasks(unfinished_tasks)
