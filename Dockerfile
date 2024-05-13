# Используем базовый образ Python
FROM python:3.9

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Копируем исходный код приложения в образ
COPY . /app

# Запускаем приложение
#CMD gunicorn main:app --bind=0.0.0.0:8080
CMD uvicorn main:app --host 0.0.0.0 --port 8080
#CMD ["python", "main.py"]