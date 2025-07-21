from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    pages: Optional[int]


class Book(BookCreate):
    id: str
