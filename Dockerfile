FROM python:3.11-slim

RUN apt-get update

RUN apt-get -y install zip

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080

ENTRYPOINT [ "python", "server.py" ]