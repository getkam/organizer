from datetime import datetime, date


def validate_date(input:str)->date:
  ''''''
  try:
    return datetime.strptime(input, "%Y-%m-%d").date()
  except ValueError: 
    raise ValueError("Wrong date format. Date should be YYYY-MM-DD")
