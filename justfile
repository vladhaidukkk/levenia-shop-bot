default: fmt lint

# Application Management
compose_file := "docker-compose-local.yaml"

up:
    docker compose -f {{compose_file}} up -d

down:
    docker compose -f {{compose_file}} down

# Code Styling
fmt:
    ruff format

lint:
    ruff check

fix:
    ruff check --fix

# Migrations Management
revise msg:
    alembic revision --autogenerate -m "{{msg}}"

migrate target="head":
    alembic upgrade {{target}}

revert target="-1":
    alembic downgrade {{target}}
