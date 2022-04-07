# API application template using FastAPI and Strawberry

## Getting started

Create `.env` file with `.env.example` keys in `config` folder.

Install dependencies:
```shell
poetry install
```

Activate virtual environment:
```shell
poetry shell
```

Make database migrations:
```shell
...
```

Create superuser for admin panel access:
```shell
...
```

Run celery task queue:
```shell
celery -A server worker -l DEBUG -P gevent  # For windows

celery -A server worker -l DEBUG  # For MacOS\Linux
```


Run server:
```shell
uvicorn app.main:app --reload
```
## Run tests
Run test and quality suits to make sure all dependencies are satisfied and applications works correctly before making changes.
```shell
pytest .
```

## GraphQL

For testing API you can follow the link `http://localhost:8000/graphql/`
