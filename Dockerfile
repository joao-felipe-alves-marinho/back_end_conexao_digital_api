# Django ninja_extra API image
FROM python:3.11.5-slim
LABEL authors="joao-felipe"

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY manage.py manage.py
COPY conexao_digital conexao_digital
COPY conexao_digital_api conexao_digital_api

COPY ./entrypoint.sh .
ENTRYPOINT ["/sh", "/app/entrypoint.sh"]
