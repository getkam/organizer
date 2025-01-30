from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, field_validator

class Task(BaseModel):
  task_id: Optional[int]
  description: str 
  due_date: date 
  priority: Literal[1, 2, 3] = 2
  is_done: bool = False

  def mark_done(self):
    self.is_done = True

  @field_validator
  def date_validator(self, due_date):
    if due_date < date.today():
      raise ValueError('Due date cannot be from the past')
    return due_date