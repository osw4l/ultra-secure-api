FROM python:3.12-alpine

ENV APP_DIR=/opt/app \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR ${APP_DIR}

RUN apk add --no-cache \
    libpq \
    postgresql-dev \
    curl \
    gettext \
    bash \
    && pip install --upgrade pip

RUN pip install --upgrade pip setuptools
COPY requirements.txt ${APP_DIR}/requirements.txt
RUN pip install -r requirements.txt

COPY apps ${APP_DIR}/apps
COPY ultra_secure_api ${APP_DIR}/ultra_secure_api
COPY templates ${APP_DIR}/templates
COPY manage.py ${APP_DIR}/manage.py

EXPOSE 9090

RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:9090"]