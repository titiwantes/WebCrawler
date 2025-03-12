FROM python:3.10

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    echo "export PATH=/root/.local/bin:$PATH" >> /root/.bashrc

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "celery", "-A", "core.celery.app", "worker", "--loglevel=info"]
