from pydantic import ValidationError
from organizer.database.db_handler import DatabaseHandler
from organizer.models.task import Task
from datetime import date

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
