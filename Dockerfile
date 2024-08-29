FROM python:3.10-slim
LABEL authors="Viktor"

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /vol/web/media

RUN addgroup --system django-group && adduser --system --ingroup django-group django-user

RUN chown -R django-user:django-group /vol/
RUN chmod -R 755 /vol/web

USER django-user
