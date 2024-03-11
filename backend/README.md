# Installation
```bash
poetry install --no-root
```

# Run server
```bash
uvicorn main:app --no-reload
```

# Database
```bash
alembic revision --autogenerate -m "create user table"
```