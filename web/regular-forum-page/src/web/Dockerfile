FROM nginx:alpine

RUN apk update && apk upgrade
RUN apk --no-cache add python3 \
    py3-greenlet py3-gevent py3-gunicorn


RUN addgroup -S app && adduser -S app -G app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY src/docker .
RUN apk --no-cache add py3-pip python3-dev && \
    pip3 install -r server-req.txt && rm server-req.txt && \
    apk del py3-pip python3-dev
RUN chmod +x *.sh && \
    mv nginx.conf /etc/nginx/nginx.conf

ENV POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres
RUN sh postgres-alpine.sh


WORKDIR /opt/ctf/app
COPY src/regularforum .
RUN rm db.sqlite3

RUN apk --no-cache add py3-pip python3-dev postgresql-dev build-base && \
    pip3 install -r requirements.txt && \
    apk del python3-dev py3-pip postgresql-dev build-base

RUN python3 manage.py collectstatic && \
    python3 manage.py makemigrations

ENV PRODUCTION=true
ENV GUNICORN_WSGI_MODULE=regularforum.wsgi:application
ENV GUNICORN_NAME=ctf GUNICORN_SOCKFILE=/run/gunicorn.sock
ENV GUNICORN_USER=nobody GUNICORN_GROUP=nobody

CMD ["/entrypoint.sh"]
