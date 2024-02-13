FROM python:3.10.12-alpine3.18
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /app/

WORKDIR /app

# Копирует все файлы из нашего локального проекта в контейнер
COPY . /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]