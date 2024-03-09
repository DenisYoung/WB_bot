# syntax=docker/dockerfile:experimental

FROM python:3.10-slim AS base

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt


COPY /bot /app

WORKDIR /app
RUN groupadd -r myuser && useradd -r -g myuser myuser
RUN chown myuser:myuser /app/celerybeat-schedule
RUN apt-get update && apt-get install -y make

CMD ["python", "mainbot.py"]
