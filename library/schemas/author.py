from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date

    model_config = ConfigDict(from_attributes=True)


class AuthorResponse(AuthorCreate):
    id: int
    first_name: str
    last_name: str
    birth_date: date

    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None

