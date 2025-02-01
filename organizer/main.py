
from datetime import date
import typer
from dashboard import show_dashboard
from tasks.task_handler import TaskHandler
from database.db_handler import DatabaseHandler
from timezone.timezone_service import time_service

app = typer.Typer()
task_handler = TaskHandler()
db_handler = DatabaseHandler()
message = None

@app.command()
def time(continent: str, city:str):
    time_service(continent, city)


@app.command()
def add(description:str, 
        due_date:str = typer.Option(None,'-d', '--due-date', help = "Date in format YYYY-MM-DD"), 
        priority: int = typer.Option(2,'-p','--priority', help="Priority of task - available values: 1, 2 ,3")):
    
    global message
    try:
        if due_date is None: 
            due_date = date.today()
        else:
            due_date = validate_date(due_date)
        task_handler.add_task(description, due_date, priority)
    except ValueError as e:
        message = e
    show_dashboard(message)

@app.command()
def delete(id:int):
    global message
    try:
        task_handler.delete_tasks([id])
    except ValueError as e:
        message = e
    show_dashboard(message)

@app.command()
def delete_done():
    global message
    try:
        task_handler.delete_done_tasks()
    except ValueError as e:
        message = e
    show_dashboard(message)

@app.command()
def show():
    global message
    show_dashboard(message)

@app.command()
def done(id:int):
    global message
    try:
        task = db_handler.get_task_by_id(id)
        task_handler.mark_task_done(task)
    except ValueError as e:
        message = e
    show_dashboard(message)

if __name__ == "__main__":
   app()