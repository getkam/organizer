import sqlite3
from datetime import date

def adapt_date(d:date) -> str:
    '''Foo to adapt objects datetime'''
    return d.isoformat()

def convert_date(date_bytes: bytes):
    '''Foo to convert from ISO (bytes) to datetime'''
    date_string = date_bytes.decode('utf-8')
    return date.fromisoformat(date_string)

# adapter registers
sqlite3.register_adapter(date, adapt_date)
sqlite3.register_converter("DATE", convert_date)
