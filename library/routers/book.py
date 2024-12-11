from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from library.database import SessionLocal
from library.models.models import Book, Author
from library.schemas.book import BookCreate, BookResponse, BookUpdate
from library.database import get_db

router = APIRouter()


@router.post(
    "/books/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавление книги",
    description="Создает новую книгу и связывает её с автором.",
)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Создание новой книги.

    - **title**: Название книги
    - **description**: Описание книги
    - **author_id**: ID автора
    - **available_copies**: Количество доступных копий
    """
    # Проверка существования автора
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Автор с ID {book.author_id} не найден."
        )

    # Создание новой книги
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
