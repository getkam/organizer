
from datetime import date
import typer
from common.helper import validate_date
from dashboard import show_dashboard
from tasks.task_handler import add_task, delete_tasks, mark_task_done, delete_done_tasks
from timezone.timezone_service import time_service

app = typer.Typer()

@app.command()
def hello(name:str):
    print(f"Hello {name}")

@app.command()
def time(continent: str, city:str):
    time_service(continent, city)


@app.command()
def add(description:str, due_date:str = typer.Option(None, help = "Date in format YYYY-MM-DD")):
    if due_date is None: 
        due_date = date.today()
    else:
        due_date = validate_date(due_date)
    add_task(description, due_date)
    show_dashboard()

@app.command()
def delete(id:int):
    delete_tasks([id])
    show_dashboard()

@app.command()
def delete_done():
    delete_done_tasks()
    show_dashboard()

@app.command()
def show():
    show_dashboard()

@app.command()
def done(id:int):
    mark_task_done(id)
    show_dashboard()

if __name__ == "__main__":
   app()