FROM python:3.11-slim

# RUN useradd -s /bin/sh -u 1234 nonroot

WORKDIR /usr/src/myapp

RUN apt-get update && apt-get install -y netcat-openbsd

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//g' /usr/src/myapp/entrypoint.sh
RUN chmod +x /usr/src/myapp/entrypoint.sh

# RUN chown -R nonroot:nonroot /usr/src/myapp
# USER nonroot

ENTRYPOINT ["./entrypoint.sh"]