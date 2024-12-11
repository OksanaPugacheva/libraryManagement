from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
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

    # Проверка на наличие книги с таким же названием и автором
    existing_book = db.query(Book).filter(
        Book.title == book.title,
        Book.author_id == book.author_id
    ).first()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Книга с названием '{book.title}' и автором ID {book.author_id} уже существует."
        )

    # Создание новой книги
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get(
    "/books/",
    response_model=List[BookResponse],
    summary="Получение списка книг",
    description="Возвращает список всех книг с доступными копиями.",
)
def get_books(db: Session = Depends(get_db)):
    """
    Возвращает список всех книг.
    """
    books = db.query(Book).all()
    return books


@router.get(
    "/books/{book_id}",
    response_model=BookResponse,
    summary="Получение информации о книге",
    description="Возвращает данные книги по её ID.",
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Возвращает данные книги по её ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга с указанным ID не найдена."
        )
    return book


@router.put(
    "/books/{book_id}",
    response_model=BookResponse,
    summary="Обновление информации о книге",
    description="Обновляет указанные данные о книге по её ID.",
)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Обновляет данные книги по её ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга с указанным ID не найдена."
        )

    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление книги",
    description="Удаляет книгу по её ID.",
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Удаляет книгу по её ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга с указанным ID не найдена."
        )

    db.delete(book)
    db.commit()
    return
