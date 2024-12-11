from fastapi import FastAPI
from library.database import init_db
from library.routers import author, book

init_db()
app = FastAPI()
app.include_router(author.router)
app.include_router(book.router)

