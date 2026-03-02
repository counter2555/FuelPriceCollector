FROM python:3.14-slim

WORKDIR /app

ADD . /app

#install curl for healthcheck
RUN apt-get -y update; apt-get -y upgrade

RUN pip install --no-cache-dir poetry

# Set the environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-ansi --no-root

CMD ["python", "run.py"]