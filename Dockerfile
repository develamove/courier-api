FROM python:3.8

# Arguments
ARG STAGE="dev"

# Environment variables
ENV STAGE ${STAGE}
ENV PYTHONUNBUFFERED 1

# Setup working directory
COPY src /app/src/
COPY .env Pipfile Pipfile.lock README.md db_manager.py wsgi.py gunicorn.conf.py app.py /app/

WORKDIR /app/

# Install libraries
RUN \
    apt-get update -y &&\
    apt-get upgrade -y &&\
    apt-get install -y groff-base &&\
    apt-get clean &&\
    pip install --upgrade setuptools wheel pip &&\
    pip install pipenv &&\
    pip install gunicorn &&\
    pip install gevent

RUN pipenv install --system --deploy

EXPOSE 8080

ENTRYPOINT ["gunicorn", "wsgi:app"]
