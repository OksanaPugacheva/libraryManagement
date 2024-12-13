from pydantic import BaseModel, ConfigDict
from typing import Optional


class BookCreate(BaseModel):
    title: str
    description: Optional[str] = None
    author_id: int
    available_copies: int = 0


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    available_copies: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author_id: int
    available_copies: int

    model_config = ConfigDict(from_attributes=True)
