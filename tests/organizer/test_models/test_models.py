import pytest
from organizer.models.task import Task
from datetime import date, timedelta
from pydantic import ValidationError

def test_task_valid_full():
  task = Task(
    description="Test task",
    priority=1,
    due_date=date.today()+ timedelta(days=3)    
  )
  assert task.task_id == None
  assert task.description == "Test task"
  assert task.priority == 1
  assert task.due_date == date.today()+ timedelta(days=3)
  assert task.is_done == False

def test_task_default_values():
  task = Task(
    description="Test default values"
  )
  assert task.task_id == None
  assert task.description == "Test default values"
  assert task.priority == 2
  assert task.due_date == date.today()
  assert task.is_done == False

@pytest.mark.parametrize("priority", [1,2,3])
def test_task_priorities(priority:int):
    task = Task(
      description="test desc",
      priority=priority
    )
    assert task.priority == priority

def test_task_invalid_priority():
  with pytest.raises(ValidationError):
    task = Task(  
      description = "Invalid task",
      priority = 4
    )
def test_task_missing_description():
  with pytest.raises(ValidationError):
    task = Task(  
      due_date = date.today()
    )

def test_task_long_description():
  task = Task(
    description='a'* 300
  )
  assert len(task.description) == 300
