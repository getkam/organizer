import time
from organizer.database.db_handler import DatabaseHandler
from organizer.models.task import Task

def test_bulk_insert_performance(in_memory_db: DatabaseHandler, sample_task:Task):
   tasks = [sample_task for _ in range(1000)]

   start_time = time.perf_counter()
   for task in tasks:
      in_memory_db.add_task(task)
   time_elapsed = time.perf_counter() - start_time

   assert time_elapsed < 1.0
   assert len(in_memory_db.get_tasks())== 1000
