# import sqlite3
# from unittest.mock import MagicMock
# sqlite3.connect = MagicMock(return_value=MagicMock())

# from typer.testing import CliRunner
# import pytest
# from organizer.main import app, task_handler
# from organizer.dashboard import show_dashboard

# def test_delete_command_success(mocker): 
#     runner = CliRunner()
#     mock_delete_tasks = mocker.patch.object(task_handler, "delete_tasks")  
#     mock_show_dashboard = mocker.patch("show_dashboard")
#     result = runner.invoke(app, ["delete", "43"])
#     assert result.exit_code == 0
#     mock_delete_tasks.assert_called_once_with([42])
#     mock_show_dashboard.assert_called_once()
