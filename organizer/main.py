
from datetime import date
import typer
from typing import Literal
from common.helper import validate_date
from dashboard import show_dashboard
from tasks.task_handler import TaskHandler
from timezone.timezone_service import time_service

app = typer.Typer()
task_handler = TaskHandler()

@app.command()
def time(continent: str, city:str):
    time_service(continent, city)


@app.command()
def add(description:str, 
        due_date:str = typer.Option(None, help = "Date in format YYYY-MM-DD"), 
        priority: int = typer.Option(2, help="Priority of task - available values: 1, 2 ,3")):
    if due_date is None: 
        due_date = date.today()
    else:
        due_date = validate_date(due_date)
    task_handler.add_task(description, due_date, priority)
    show_dashboard()

@app.command()
def delete(id:int):
    task_handler.delete_tasks([id])
    show_dashboard()

@app.command()
def delete_done():
    task_handler.delete_done_tasks()
    show_dashboard()

@app.command()
def show():
    show_dashboard()

@app.command()
def done(id:int):
    task_handler.mark_task_done(id)
    show_dashboard()

if __name__ == "__main__":
   app()