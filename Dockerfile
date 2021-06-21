# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
RUN apt update && apt upgrade -y
WORKDIR /opt/app
COPY requirements.txt /opt/app/
RUN pip install -r requirements.txt
COPY . /opt/app
RUN rm -rf /opt/app/data/*.sqlite3

EXPOSE 8000

ENTRYPOINT ["./manage.py", "runserver", "0.0.0.0:8000"]
