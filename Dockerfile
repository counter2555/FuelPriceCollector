FROM python:3.14-slim

WORKDIR /app

# 1. Install Poetry first
RUN pip install --no-cache-dir poetry

# 2. Copy ONLY the dependency files
# This allows Docker to cache the 'install' step
COPY pyproject.toml poetry.lock* /app/

# 3. Install dependencies 
# (virtualenvs.create false ensures they go into the system python)
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi --no-root

# 4. NOW copy your main.py and other files
COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]