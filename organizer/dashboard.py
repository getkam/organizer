from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich import print
from datetime import date

from organizer.database.db_handler import DatabaseHandler
from organizer.weather.weather_service import get_weather
from organizer.currency.currency_service import get_currency
from organizer.models.weather import Weather
database_handler = DatabaseHandler()

def show_dashboard(message: str):
    tasks = database_handler.get_tasks()

    console = Console()

    layout = Layout()
    layout.split_column(
        Layout(name="top", size=7),
        Layout(name="body"),

    )

    layout["top"].split_row(
        Layout(name="top-left"),
        Layout(name="top-center"),
        Layout(name="top-right")
    )
    weather:Weather = get_weather()
    weather_box=f"""
        Current temperature: {weather.current} \u00B0C
        Feels like: {weather.feel_like} \u00B0C
        {weather.get_icon()} {weather.weather_description}
        """
    layout["top-left"].update(Panel(weather_box,title="Weather"))

    currency = get_currency()
    currency_box = f"""
        PLN/EUR: {currency["EUR"]}
        PLN/USD: {currency["USD"]}
    """
    layout["top-center"].update(Panel(currency_box, title="Currencies"))



    layout["top-right"].update(Panel("", title="Time"))
    if message: 
        print(message)

    table = Table(expand=True, leading=1, border_style="frame")
    table.add_column("ID", justify="right", style="white", no_wrap=True, ratio=1)
    table.add_column("DESCRIPTION", style="white", ratio=10)
    table.add_column("DUE DATE", style="white",ratio=2)
    table.add_column("PRIORITY", justify="center",ratio=1)
    table.add_column("DONE", justify="center",style="white", ratio=1)

    for task in tasks:
    
        done = '✅' if task.is_done == 1 else '⬜'
        priority = '🔥' if task.priority == 1 else '🔵' if task.priority == 2 else '⬇️' 

        row_color = color(task.due_date, task.is_done)
        table.add_row(str(task.task_id), task.description, str(task.due_date), priority, done, style=row_color)

    layout["body"].update(Panel(table,title="TODO List"))
    print(layout)

def color(task_date:date, done):
    row_color = "white"
    if task_date < date.today():
        row_color = "#F07080"
    if done == 1: 
        row_color = "green"
    return row_color