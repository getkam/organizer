from organizer.database.db_handler import DatabaseHandler
from organizer.models.task import Task


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