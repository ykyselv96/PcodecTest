from datetime import date

from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    published_date: date
    isbn: str
    pages: str

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published_date: Optional[date]
    isbn: Optional[str]
    pages: Optional[str]
