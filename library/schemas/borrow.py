from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


# Модель для возврата книги
class BorrowReturn(BaseModel):
    return_date: datetime
