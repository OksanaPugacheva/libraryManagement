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

## Установка и запуск

### Требования

- **Python 3.11+**
- **Docker** и **Docker Compose**
- Установленные зависимости из `requirements.txt`

---

### Запуск с использованием Docker

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/library-management.git
   cd library-management
2. Соберите контейнеры:
   ```bash
   docker-compose build
3. Запустите приложение:
   ```bash
   docker-compose up
4. API будет доступно по адресу http://localhost:8000.

## Документация API
Встроенная документация доступна по следующим адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Использование Postman

В проекте доступна коллекция базовых запросов Postman для тестирования API.

1. Скачайте коллекцию из папки [`postman`](./postman/library_management_collection.json).
2. Импортируйте коллекцию в Postman:
   - Откройте Postman.
   - Нажмите **Import** → **Upload Files** → выберите файл `library_management_collection.json`.
3. Тестируйте API