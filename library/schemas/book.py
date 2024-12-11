from pydantic import BaseModel
from datetime import date
from typing import Optional


class BookCreate(BaseModel):
    title: str
    description: Optional[str] = None
    author_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class BookResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author_id: int

    class Config:
        orm_mode = True
