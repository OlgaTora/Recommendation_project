FROM python:3.10.12-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY ./requirements.txt /app/
WORKDIR /app
COPY . /app/
RUN apt-get update && apt-get install -y gcc && \
    apt-get install -y default-libmysqlclient-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt