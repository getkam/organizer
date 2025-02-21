from datetime import date
from unittest.mock import MagicMock
import pytest

from organizer.models.task import Task


def test_add_task_with_defaults(task_handler, mock_db_handler):
    #Act
    task_handler.add_task("test")

    #Assert
    mock_db_handler.add_task.assert_called_once()
    added_task:Task = mock_db_handler.add_task.call_args[0][0]

    assert added_task.description == "test"
    assert added_task.priority == 2
    assert added_task.due_date == date.today()
    assert added_task.is_done == False


def test_add_task_custom(task_handler, mock_db_handler):
  
    task_handler.add_task(description="task", due_date=date(2025, 10, 10), priority=1)

    mock_db_handler.add_task.assert_called_once()
    added_task:Task = mock_db_handler.add_task.call_args[0][0]

    assert added_task.description == "task"
    assert added_task.due_date == date(2025, 10, 10)
    assert added_task.priority == 1
    assert added_task.is_done == False


@pytest.mark.parametrize("due_date",[date.min, date(2024,2,29),date.max])
def test_add_task_edge_due_dates(task_handler, mock_db_handler, due_date: date):
    #Act 
    task_handler.add_task("test", due_date=due_date)
    
    #Assert
    mock_db_handler.add_task.assert_called_once()
    added_task:Task = mock_db_handler.add_task.call_args[0][0]

    assert added_task.due_date == due_date


@pytest.mark.parametrize("priority",[1,2,3])
def test_add_task_checking_priority(task_handler, mock_db_handler, priority: int):

    #Act 
    task_handler.add_task("test", priority=priority)
    
    #Assert
    mock_db_handler.add_task.assert_called_once()
    added_task:Task = mock_db_handler.add_task.call_args[0][0]

    assert added_task.priority == priority


@pytest.mark.parametrize("priority",[-1,0,4])
def test_add_task_invalid_priority(task_handler, mock_db_handler, priority: int):

    #Assert
    with pytest.raises(ValueError):
      task_handler.add_task("test", priority=priority)
    
    mock_db_handler.add_task.assert_not_called()
    

def test_add_task_missing_description(task_handler, mock_db_handler):

    #Assert
    with pytest.raises(TypeError):
      task_handler.add_task()
    
    mock_db_handler.add_task.assert_not_called()


def test_delete_tasks_existing(task_handler, mock_db_handler):
    #Arrange
    ids = [1,3,67]

    #Act
    task_handler.delete_tasks(ids)

    #Assert
    mock_db_handler.delete_tasks.assert_called_once_with(ids)


def test_delete_task_empty_list(task_handler, mock_db_handler):

    #Act
    task_handler.delete_tasks([])

    #Assert
    mock_db_handler.delete_tasks.assert_called_once_with([])


def test_mark_task_done(task_handler, mock_db_handler):
    #Arrange
    task = Task(task_id=12, description="desc")

    #Act
    task_handler.mark_task_done(task)

    #Assert
    mock_db_handler.mark_task_done.assert_called_once()
    marked_task_id = mock_db_handler.mark_task_done.call_args[0][0]
    assert marked_task_id == task.task_id



def test_delete_done_tasks(task_handler, mock_db_handler):
    #Arrange
    mock_task1 = MagicMock(task_id = 1, is_done = 1)
    mock_task2 = MagicMock(task_id = 2, is_done = 0)
    expected_ids = [1]
    mock_db_handler.get_tasks.return_value = [mock_task1, mock_task2]

    #Act
    task_handler.delete_done_tasks()
    
    #Assert
    mock_db_handler.get_tasks.assert_called_once()
    mock_db_handler.delete_tasks.assert_called_once_with(expected_ids)

def test_delete_done_tasks_nothing_done(task_handler, mock_db_handler):
    #Arrange
    mock_task1 = MagicMock(task_id = 1, is_done = 0)
    mock_task2 = MagicMock(task_id = 2, is_done = 0)
    expected_ids = []
    mock_db_handler.get_tasks.return_value = [mock_task1, mock_task2]

    #Act
    task_handler.delete_done_tasks()
    
    #Assert
    mock_db_handler.get_tasks.assert_called_once()
    mock_db_handler.delete_tasks.assert_called_once_with(expected_ids)

def test_delete_done_tasks_everything_done(task_handler, mock_db_handler):
    #Arrange
    mock_task1 = MagicMock(task_id = 1, is_done = 1)
    mock_task2 = MagicMock(task_id = 2, is_done = 1)
    expected_ids = [1,2]
    mock_db_handler.get_tasks.return_value = [mock_task1, mock_task2]

    #Act
    task_handler.delete_done_tasks()
    
    #Assert
    mock_db_handler.get_tasks.assert_called_once()
    mock_db_handler.delete_tasks.assert_called_once_with(expected_ids)
