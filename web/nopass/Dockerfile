FROM python:3.8-alpine3.12

RUN apk update && \
    apk add --update alpine-sdk sqlite

WORKDIR /opt/nopass_login
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY web/fixtures ./fixtures
COPY web/nopass_login ./nopass_login
COPY web/manage.py .
RUN mkdir db

RUN python3 manage.py migrate
RUN python3 manage.py loaddata admin

RUN adduser --disabled-password compfest12

RUN chmod -R 555 .
RUN chmod -R 777 db

USER compfest12

EXPOSE 8000

ENTRYPOINT [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]