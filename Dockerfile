FROM python:3.11-slim

WORKDIR /core

COPY requirements.txt /core/

RUN pip install --upgrade pip && \
    pip install poetry && \
    useradd -m core && \
    chown -R crawler-legal-processes.core /core && \
    cd /core && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

USER crawler_processes

ADD . /core/
