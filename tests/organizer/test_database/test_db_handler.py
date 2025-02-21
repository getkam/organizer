import pytest
from pydantic import ValidationError
from organizer.database.db_handler import DatabaseHandler
from organizer.models.task import Task
from datetime import date

def test_add_task(in_memory_db: DatabaseHandler, sample_task:Task): 
  in_memory_db.add_task(sample_task)

  with in_memory_db.connection as conn:
      retrieved_task = conn.execute('''
                                    SELECT id, description, due_date, priority, is_done 
                                    FROM tasks 
                                    WHERE id = ?
                                    ''', [1]).fetchone()
      assert retrieved_task['description'] == sample_task.description
      assert retrieved_task['due_date'] == sample_task.due_date
      assert retrieved_task['priority'] == sample_task.priority
      assert retrieved_task['is_done'] == False

def test_add_task_default_values(in_memory_db: DatabaseHandler):
   task = Task(
      description="only description"
   )
   in_memory_db.add_task(task)
   with in_memory_db.connection as conn:
      retrieved_task = conn.execute('''
                                    SELECT id, description, due_date, priority, is_done 
                                    FROM tasks 
                                    WHERE id = ?
                                    ''', [1]).fetchone()
      assert retrieved_task['description'] == task.description
      assert retrieved_task['due_date'] == date.today()
      assert retrieved_task['priority'] == 2
      assert retrieved_task['is_done'] == False

def test_auto_increment(in_memory_db: DatabaseHandler, sample_task:Task):
  in_memory_db.add_task(sample_task)
  in_memory_db.add_task(sample_task)

  with in_memory_db.connection as conn:
   retrieved_tasks = conn.execute('''
                                    SELECT id, description, due_date, priority, is_done 
                                    FROM tasks 
                                    ''').fetchall()
   
  assert [t['id'] for t in retrieved_tasks] == [1, 2]

def test_long_description(in_memory_db: DatabaseHandler):
   task = Task(
      description='A' * 300
   )
   in_memory_db.add_task(task)

   with in_memory_db.connection as conn:
      retrieved_task = conn.execute('''
                                    SELECT id, description, due_date, priority, is_done 
                                    FROM tasks 
                                    WHERE id = ?
                                    ''', [1]).fetchone()
      assert len(retrieved_task['description']) == 300

def test_date_edge_case(in_memory_db: DatabaseHandler):
   edge_dates = [
      date.min,
      date.max, 
      date(2024,2,29)
   ]
   for e in edge_dates:
      in_memory_db.add_task(Task(description="task", due_date=e))
   
   with in_memory_db.connection as conn:
      retrieved_tasks = conn.execute('''
                                    SELECT id, description, due_date, priority, is_done 
                                    FROM tasks 
                                    ''').fetchall()
   for i, task in enumerate(retrieved_tasks):
      assert task['due_date'] == edge_dates[i]

def test_add_task_missing_required(in_memory_db: DatabaseHandler):
   with pytest.raises(ValidationError):
      in_memory_db.add_task(Task(due_date=date.today()))


def test_get_task_by_id_positive(in_memory_db:DatabaseHandler, one_task_in_db:Task):
   retrieved_task = in_memory_db.get_task_by_id(1)
   assert retrieved_task.task_id == 1
   assert retrieved_task.description == one_task_in_db.description
   assert retrieved_task.priority == one_task_in_db.priority
   assert retrieved_task.due_date == one_task_in_db.due_date
   assert retrieved_task.is_done == one_task_in_db.is_done

def test_get_task_by_id_negative(in_memory_db:DatabaseHandler):
   with pytest.raises(ValueError):
      in_memory_db.get_task_by_id(1)

def test_delete_tasks(in_memory_db:DatabaseHandler, ten_tasks_in_db:list[Task]):
   deleted_tasks =[1,3,5,7,9]
   in_memory_db.delete_tasks(deleted_tasks)

   with in_memory_db.connection as conn:
      retrieved_tasks = conn.execute('''
                                       SELECT id FROM tasks
                                     ''').fetchall()
   remained_ids = [t['id'] for t in retrieved_tasks]
   assert deleted_tasks not in remained_ids 
   assert [i + 1 for i in range(10) if i+1 not in deleted_tasks] == remained_ids


def test_delete_tasks_missing_param(in_memory_db:DatabaseHandler):
   with pytest.raises(ValueError): 
      in_memory_db.delete_tasks([])
   

def test_delete_task_not_existing(in_memory_db:DatabaseHandler,ten_tasks_in_db:list[Task]):
   in_memory_db.delete_tasks([1,2,5,7,9, 13, 16, 456])
   with in_memory_db.connection as conn:
      retrieved_tasks = conn.execute('''SELECT id FROM tasks''').fetchall()

   remained_id = [t['id'] for t in retrieved_tasks]
   assert [3, 4, 6, 8, 10] == remained_id, f"Expected [3, 4, 6, 8, 10], but found {remained_id}."


def test_mark_test_done_positive(in_memory_db:DatabaseHandler, one_task_in_db:Task):
   in_memory_db.mark_task_done(1)
   with in_memory_db.connection as conn:
      retrieved_task = conn.execute('''SELECT * 
                                       FROM tasks
                                       WHERE id = 1
                                       ''').fetchone()
   assert retrieved_task['is_done'], f"Expected that for task id = 1 attribute is_done=True, but was False."

def test_mark_test_done_not_existed(in_memory_db:DatabaseHandler): 
   id = 10
   with pytest.raises(ValueError, match=f"Task with id {id} doesn't exist"):
      in_memory_db.mark_task_done(id)

def test_is_exist_positive(in_memory_db:DatabaseHandler, one_task_in_db:Task):
   assert in_memory_db.id_exist(1)

def test_is_exist_negative(in_memory_db:DatabaseHandler):
   assert not in_memory_db.id_exist(1)
   