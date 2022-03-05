# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
RUN apt update && apt upgrade -y
RUN apt install -y gcc libmariadbclient-dev libsqlite3-dev libpq-dev
WORKDIR /opt/app
COPY requirements.txt /opt/app/
RUN pip install -r requirements.txt
COPY . /opt/app
RUN rm -rf /opt/app/data/*.sqlite3

EXPOSE 8000

ENTRYPOINT ["./scripts/prod_deploy.sh"]
