from database.db_handler import get_tasks, add_task_db, delete_tasks_db, mark_task_done_db
from datetime import date


def add_task(description:str, scheduled:date):
    add_task_db(description, scheduled)

def delete_tasks(ids):
    delete_tasks_db(ids)


def mark_task_done(id:int):
    mark_task_done_db(id)

def delete_done_tasks():
    tasks = get_tasks()
    unfinished_tasks = [task[0] for task in tasks if task[3] == 1]
    delete_tasks(unfinished_tasks)
