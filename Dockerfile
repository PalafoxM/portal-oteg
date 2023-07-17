FROM python:3.9-alpine

RUN apk update && apk add mysql-client py3-pip py3-pillow py3-cffi py3-brotli gcc musl-dev python3-dev pango py3-mysqlclient mariadb-dev build-base

WORKDIR /usr/src/app
COPY requirements/requirements.txt ./
RUN pip install weasyprint
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]