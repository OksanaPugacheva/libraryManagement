# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /libraryManagementApp

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY library /libraryManagementApp/library

# Указываем рабочую директорию для запуска приложения
WORKDIR /libraryManagementApp

# Открываем порт для доступа к приложению
EXPOSE 8000

# Указываем команду для запуска приложения
CMD ["uvicorn", "library.main:app", "--host", "0.0.0.0", "--port", "8000"]
