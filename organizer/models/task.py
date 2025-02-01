from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, field_validator

class Task(BaseModel):
  task_id: Optional[int] = None
  description: str 
  due_date: date 
  priority: Literal[1, 2, 3] = 2
  is_done: bool = False

  def mark_done(self):
    self.is_done = True
