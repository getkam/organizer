import pytest
from unittest.mock import Mock
from organizer.tasks.task_handler import TaskHandler
from organizer.database.db_handler import DatabaseHandler
from organizer.models.task import Task

@pytest.fixture(scope="function")
def mock_db_handler():
  return Mock()

@pytest.fixture(scope="function")
def task_handler(mock_db_handler: DatabaseHandler):
  handler = TaskHandler(mock_db_handler)
  return handler