import pytest
import sqlite3
import time
from pydantic import ValidationError
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

def test_add_task(in_memory_db: DatabaseHandler, sample_task:Task): 

  in_memory_db.add_task(sample_task)

  retrieved_task = in_memory_db.get_task_by_id(1)
  assert retrieved_task.description == sample_task.description
  assert retrieved_task.due_date == sample_task.due_date
  assert retrieved_task.priority == sample_task.priority
  assert retrieved_task.is_done == False


def test_add_task_default_values(in_memory_db: DatabaseHandler):
   task = Task(
      description="only description"
   )
   in_memory_db.add_task(task)
   retrieved_task = in_memory_db.get_task_by_id(1)
   assert retrieved_task.description == task.description
   assert retrieved_task.due_date == date.today()
   assert retrieved_task.priority == 2
   assert retrieved_task.is_done == False

def test_add_task_many(in_memory_db: DatabaseHandler, sample_task:Task):

  in_memory_db.add_task(sample_task)
  in_memory_db.add_task(sample_task)

  retrieved_tasks = in_memory_db.get_tasks()
  assert  [t.task_id for t in retrieved_tasks] == [1, 2]

def test_long_description(in_memory_db: DatabaseHandler):
   
   task = Task(
      description='A' * 255
   )
   in_memory_db.add_task(task)

   retrieved_task = in_memory_db.get_task_by_id(1)
   assert len(retrieved_task.description) == 255

def test_invalid_priority(in_memory_db: DatabaseHandler):
   with pytest.raises(ValidationError):
      in_memory_db.add_task(Task(
            description = "Invalid priority",
            priority = 4
   ))

def test_date_edge_case(in_memory_db: DatabaseHandler):
   edge_dates = [
      date.min,
      date.max, 
      date(2024,2,29)
   ]
   for e in edge_dates:
      in_memory_db.add_task(Task(description="task", due_date=e))
   
   retrieved_tasks = in_memory_db.get_tasks()
   for i, task in enumerate(retrieved_tasks):
      assert task.due_date == edge_dates[i]

def test_missing_required(in_memory_db: DatabaseHandler):
   with pytest.raises(ValidationError):
      in_memory_db.add_task(Task(due_date=date.today()))

def test_sql_injection_attempt(in_memory_db: DatabaseHandler):
   malicious_desc = "Task'); DROP TABLE tasks;--"
   task = Task(
      description=malicious_desc
   )
   in_memory_db.add_task(task)

   with in_memory_db.connection as conn:
      tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
      tables_list = [row["name"] for row in tables]
      assert "tasks" in tables_list

   retrieve_task = in_memory_db.get_task_by_id(1)
   assert retrieve_task.description == malicious_desc

def test_bulk_insert_performance(in_memory_db: DatabaseHandler, sample_task:Task):
   tasks = [sample_task for _ in range(1000)]

   start_time = time.perf_counter()
   for task in tasks:
      in_memory_db.add_task(task)
   time_elapsed = time.perf_counter() - start_time

   assert time_elapsed < 1.0
   assert len(in_memory_db.get_tasks())== 1000

def test_transaction_rollback(in_memory_db: DatabaseHandler):

   try:
      in_memory_db.add_task(Task(
      description="Valid task",
      due_date = date.today(),
      priority=1
   ))
      in_memory_db.add_task(Task(
      description="Invalid task",
      due_date=date.today(),
      priority=0
   ))
   except ValidationError:
      pass
   
   tasks = in_memory_db.get_tasks()

   assert len(tasks) == 1
   assert "Valid task" in [task.description for task in tasks]