from rich.console import Console
from rich.table import Table
from database.db_handler import DatabaseHandler
from datetime import date

database_handler = DatabaseHandler()

def show_dashboard(message: str):
    tasks = database_handler.get_tasks()

    console = Console()
    console.clear()
    if message: 
        print(message)
    table = Table(title="*** LIST OF TASKS ***")

    table.add_column("ID", justify="right", style="white", no_wrap=True)
    table.add_column("DESCRIPTION", style="white")
    table.add_column("DUE DATE", style="white")
    table.add_column("PRIORITY", justify="center", style="white")
    table.add_column("DONE", justify="center",style="white")

    for task in tasks:
    
        done = '✅' if task.is_done == 1 else '⬜'
        priority = '🔥' if task.priority == 1 else '🔵' if task.priority == 2 else '⬇️' 

        row_color = color(task.due_date, task.is_done)
        table.add_row(str(task.task_id), task.description, str(task.due_date), priority, done, style=row_color)

    console.print(table)


def color(task_date:date, done):
    row_color = "white"
    if task_date < date.today():
        row_color = "#F07080"
    if done == 1: 
        row_color = "green"
    return row_color