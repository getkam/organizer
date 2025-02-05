import pytest
import sqlite3
from organizer.database.db_handler import DatabaseHandler
from organizer.models.task import Task
from datetime import date, timedelta


def adapt_date(d:date) -> str:
    '''Foo to adapt objects datetime'''
    return d.isoformat()

def convert_date(date_bytes: bytes):
    '''Foo to convert from ISO (bytes) to datetime'''
    date_string = date_bytes.decode('utf-8')
    return date.fromisoformat(date_string)

# adapter registers
sqlite3.register_adapter(date, adapt_date)
sqlite3.register_converter("DATE", convert_date)


@pytest.fixture(scope="function")
def in_memory_db():
  handler = DatabaseHandler(db_path=":memory:")
  with handler.connection as connection:
    connection.execute('''
                      CREATE TABLE tasks(
                      id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      description TEXT NOT NULL, 
                      due_date DATE NOT NULL,
                      priority INTEGER CHECK(priority IN (1, 2, 3)) DEFAULT 2,
                      is_done BOOLEAN NOT NULL DEFAULT 0
                      )
                      ''')
  yield handler
  handler.close_connection()

@pytest.fixture()
def sample_task(in_memory_db: DatabaseHandler) -> Task:
  task = Task(
    description="seeded task",
    due_date = date.today() + timedelta(days = 1),
    priority = 1
  )
  return task

@pytest.fixture()
def one_task_in_db(in_memory_db: DatabaseHandler) -> Task:
  task = Task(
    description="seeded task",
    due_date = date.today() + timedelta(days = 1),
    priority = 1
  )
  in_memory_db.add_task(task)
  return task


@pytest.fixture()
def ten_tasks_in_db(in_memory_db: DatabaseHandler) -> list[Task]:
  tasks = [Task(
    description="seeded task",
    due_date = date.today() + timedelta(days = 1),
    priority = 1
  ) for _ in range(10)]

  for task in tasks:
     in_memory_db.add_task(task)
  return tasks