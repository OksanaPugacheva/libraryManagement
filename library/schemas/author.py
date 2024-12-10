from pydantic import BaseModel
from datetime import date


# Pydantic схема для запроса нового автора
class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date

    class Config:
        orm_mode = True


class AuthorResponse(AuthorCreate):
    id: int
    first_name: str
    last_name: str
    birth_date: date

    class Config:
        orm_mode = True
