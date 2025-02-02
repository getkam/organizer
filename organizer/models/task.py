from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel

class Task(BaseModel):
  task_id: Optional[int] = None
  description: str 
  due_date: Optional[date] = date.today() 
  priority: Optional[Literal[1, 2, 3]] = 2
  is_done: Optional[bool] = False

  def mark_done(self):
    self.is_done = True
