{% for field in filter.form %}
            <div id="form-field-{{ forloop.counter0 }}">
                {{ field.label_tag }}
                {% render_field field class="form-control" %}
            </div>
            {% endfor %}
FROM python:3.10.12-alpine3.18
ENV PYTHONUNBUFFERED 1

# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /recommendations

COPY requirements.txt requirements.txt

# Копирует все файлы из нашего локального проекта в контейнер
ADD ./recommendations

RUN pip install pip==23.1.2
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

FROM apache/airflow:2.7.1
COPY ./.env ./
COPY ./docker/airflow/requirements.txt ./
RUN pip install pip==23.1.2
RUN pip install --no-cache-dir -r requirements.txt
COPY ./dags ./dags

ADD . /app
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/dags"
