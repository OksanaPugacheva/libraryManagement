from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from library.database import SessionLocal
from library.models.models import Author
from library.schemas.author import AuthorCreate, AuthorResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = Author(first_name=author.first_name, last_name=author.last_name, birth_date=author.birth_date)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author
