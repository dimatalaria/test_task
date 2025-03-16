FROM python:3.12-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y netcat-openbsd

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY ./fastapi-application ./

CMD python3 -m uvicorn main:main_app --reload --host 0.0.0.0 --port 8002