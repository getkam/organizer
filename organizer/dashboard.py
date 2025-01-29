from rich.console import Console
from rich.table import Table
from database.db_handler import get_tasks
from datetime import date
from common.helper import validate_date


def show_dashboard():
    tasks = get_tasks()

    console = Console()
    table = Table(title="List of Tasks")

    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("DESCRIPTION", style="white")
    table.add_column("DUE DATE", style="white")
    table.add_column("DONE", justify="center",style="white")

    for task in tasks:
        task_id, task_desc, task_date, task_done = task
    
        done = '✅' if task_done == 1 else '⬜'

        row_color = color(task_date, task_done)

        table.add_row(str(task_id), task_desc, task_date, done, style=row_color)

    console.print(table)


def color(task_date, done):
    row_color = "white"
    due_date = validate_date(task_date)
    if due_date < date.today():
        row_color = "red"

    if done == 1: 
        row_color = "green"

    return row_color