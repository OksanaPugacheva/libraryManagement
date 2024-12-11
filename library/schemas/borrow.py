from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BorrowCreate(BaseModel):
    book_id: int
    reader_name: str


class BorrowResponse(BaseModel):
    id: int
    book_id: int
    reader_name: str
    borrow_date: datetime
    return_date: Optional[datetime]

    class Config:
        orm_mode = True


# Модель для возврата книги
class BorrowReturn(BaseModel):
    return_date: datetime
