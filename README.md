# API для управления библиотекой
## Обзор
Проект представляет собой API для управления библиотекой, созданное с использованием
FastAPI и SQLAlchemy (v2). Оно предоставляет RESTful эндпоинты для управления авторами,
книгами и записями о выдаче, а также функциональность для выдачи и возврата книг.

## Бизнес-логика
1. Создание записи о выдаче:
   - Проверяется наличие доступных экземпляров книги. 
   - Если экземпляров нет, возвращается ошибка.
2. При выдаче книги:
   - Количество доступных экземпляров книги уменьшается на 1.
3. При возврате книги:
   - Количество доступных экземпляров книги увеличивается на 1. 
   - Устанавливается дата возврата, переданная в запросе.