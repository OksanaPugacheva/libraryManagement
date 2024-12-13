from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from library.models.models import Book, Borrow
from library.schemas.borrow import BorrowCreate, BorrowResponse, BorrowReturn
from library.database import get_db

router = APIRouter()


@router.post(
    "/borrows/",
    response_model=BorrowResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание записи о выдаче книги",
    description="Создает запись о выдаче книги, проверяя наличие экземпляров.",
)
def create_borrow(borrow: BorrowCreate, db: Session = Depends(get_db)):
    """
    Создание новой записи о выдаче книги.

    - Проверяет наличие экземпляров книги.
    - Уменьшает количество доступных экземпляров.
    """
    # Проверяем наличие книги
    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {borrow.book_id} не найдена."
        )

    # Проверяем доступные экземпляры
    if book.available_copies < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Нет доступных экземпляров книги '{book.title}'."
        )

    # Уменьшаем количество доступных экземпляров
    book.available_copies -= 1

    # Создаем запись о выдаче
    new_borrow = Borrow(**borrow.dict())
    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)

    return new_borrow


@router.get(
    "/borrows/",
    response_model=List[BorrowResponse],
    summary="Получение списка всех выдач",
    description="Возвращает список всех записей о выдачах.",
)
def get_borrows(db: Session = Depends(get_db)):
    """
    Возвращает список всех записей о выдачах.
    """
    borrows = db.query(Borrow).all()
    return borrows


@router.get(
    "/borrows/{borrow_id}",
    response_model=BorrowResponse,
    summary="Получение информации о выдаче",
    description="Возвращает информацию о выдаче по ID.",
)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    """
    Возвращает информацию о выдаче книги ID.
    """
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о выдаче не найдена."
        )
    return borrow


@router.patch(
    "/borrows/{borrow_id}/return",
    response_model=BorrowResponse,
    summary="Завершение выдачи",
    description="Завершает выдачу книги, увеличивая количество доступных экземпляров.",
)
def return_borrow(
        borrow_id: int,
        return_data: BorrowReturn,
        db: Session = Depends(get_db)
):
    """
    Завершает выдачу книги.

    - Увеличивает количество доступных экземпляров книги.
    - Устанавливает дату возврата, переданную в запросе.
    """
    # Находим запись о выдаче
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о выдаче не найдена."
        )

    # Проверяем, была ли книга уже возвращена
    if borrow.return_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга уже возвращена."
        )

    # Увеличиваем количество доступных экземпляров книги
    book = db.query(Book).get(borrow.book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {borrow.book_id} не найдена."
        )
    else:
        book.available_copies += 1

    # Устанавливаем дату возврата, переданную в запросе
    borrow.return_date = return_data.return_date
    db.commit()
    db.refresh(borrow)

    return borrow
