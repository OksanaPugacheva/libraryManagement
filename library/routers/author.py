from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from library.database import SessionLocal
from library.models.models import Author
from library.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/authors/",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание автора",
    description="Создает нового автора с указанными именем, фамилией и датой рождения, если такого автора еще нет.",
    response_description="Возвращает данные созданного автора."
)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """
    Создание нового автора.

    - **first_name**: Имя автора (обязательно)
    - **last_name**: Фамилия автора (обязательно)
    - **birth_date**: Дата рождения автора (обязательно)
    """

    # Проверяем наличие автора в базе данных
    existing_author = db.query(Author).filter(
        Author.first_name == author.first_name,
        Author.last_name == author.last_name,
        Author.birth_date == author.birth_date
    ).first()

    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Автор с таким именем, фамилией и датой рождения уже существует."
        )

    # Добавляем нового автора
    new_author = Author(first_name=author.first_name, last_name=author.last_name, birth_date=author.birth_date)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


@router.get(
    "/authors/",
    response_model=List[AuthorResponse],  # Список объектов AuthorResponse
    summary="Получение списка авторов",
    description="Возвращает список всех авторов.",
    response_description="Список авторов с их данными."
)
def get_authors(db: Session = Depends(get_db)):
    """
    Возвращает список всех авторов.

    - Поля в ответе:
        - **id**: Уникальный идентификатор автора
        - **first_name**: Имя автора
        - **last_name**: Фамилия автора
        - **birth_date**: Дата рождения автора
    """
    authors = db.query(Author).all()
    return authors


@router.get(
    "/authors/{author_id}",
    response_model=AuthorResponse,  # Возвращаемый объект соответствует модели AuthorResponse
    summary="Получение информации об авторе",
    description="Возвращает данные автора по его уникальному идентификатору.",
    response_description="Данные автора."
)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Возвращает информацию об авторе по ID.

    - **id**: Уникальный идентификатор автора
    - Возвращаемые поля:
        - **id**: Уникальный идентификатор
        - **first_name**: Имя автора
        - **last_name**: Фамилия автора
        - **birth_date**: Дата рождения автора
    """
    # Поиск автора по ID
    author = db.query(Author).filter(Author.id == author_id).first()

    # Если автор не найден, выбрасываем исключение
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автор с указанным ID не найден."
        )

    return author


@router.put(
    "/authors/{author_id}",
    response_model=AuthorResponse,
    summary="Обновление информации об авторе",
    description="Обновляет данные автора (имя, фамилию или дату рождения) по его уникальному идентификатору.",
    response_description="Обновленные данные автора."
)
def update_author(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
    """
    Частичное обновление информации об авторе по ID.

    - **author_id**: Уникальный идентификатор автора
    - Поля для обновления (все опциональны):
        - **first_name**: Новое имя автора
        - **last_name**: Новая фамилия автора
        - **birth_date**: Новая дата рождения автора
    """

    # Проверяем, существует ли автор
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автор с указанным ID не найден."
        )

    # Составляем словарь изменений
    updates = {key: value for key, value in author_update.dict(exclude_unset=True).items()}

    # Выполняем обновление
    db.query(Author).filter(Author.id == author_id).update(updates)
    db.commit()

    # Получаем обновленные данные
    db.refresh(author)
    return author
