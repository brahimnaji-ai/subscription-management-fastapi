# Subscription Management API

## Purpose

Subscription Management API is a realistic FastAPI backend for learning Python and FastAPI through concepts that are familiar from Java and Spring Boot. The application models the plan-management part of a SaaS subscription system while keeping HTTP, business, and persistence concerns separate.

## Tech stack

- Python 3.14
- FastAPI
- uv for dependency and environment management
- SQLAlchemy 2.x
- PostgreSQL
- psycopg
- Alembic
- Pydantic
- pytest when automated tests are introduced

## Architecture

```text
Router -> Service -> Repository -> SQLAlchemy -> PostgreSQL
```

- **Router** handles HTTP details, dependency injection, status codes, and conversion to response schemas.
- **Service** contains business rules and coordinates transaction boundaries.
- **Repository** owns persistence queries and writes through a SQLAlchemy session.
- **SQLAlchemy models** describe the database representation.
- **Pydantic schemas** define the public request and response contracts.
- **Alembic** applies versioned database-schema changes.

This separation keeps persistence models from becoming the public API contract.

## Project structure

```text
.
|-- alembic/
|   |-- versions/
|   |   `-- c8b447c63995_create_plans_table.py
|   |-- env.py
|   `-- script.py.mako
|-- app/
|   |-- api/
|   |   |-- v1/
|   |   |   `-- plan_router.py
|   |   `-- router.py
|   |-- db/
|   |   |-- base.py
|   |   `-- database.py
|   |-- models/
|   |   `-- plan.py
|   |-- repository/
|   |   `-- plan_repository.py
|   |-- schemas/
|   |   `-- plan.py
|   |-- service/
|   |   `-- plan_service.py
|   `-- main.py
|-- alembic.ini
|-- pyproject.toml
`-- uv.lock
```

Package `__init__.py` files are omitted from the diagram for readability.

## Database mental model

```text
FastAPI request
      |
      v
SQLAlchemy Session
      |
      v
SQLAlchemy Engine
      |
      v
PostgreSQL
```

The engine manages database connectivity and connection pooling. A session is a unit of work that tracks ORM objects and provides a transaction boundary. ORM models map Python classes to database tables, while Alembic manages the evolution of those tables through migrations.

For developers coming from Spring Boot, the following comparisons can be useful mental models, although the components are not technically identical:

| Python/FastAPI | Rough Spring Boot comparison |
|---|---|
| SQLAlchemy Engine | `DataSource` |
| SQLAlchemy Session | `EntityManager` |
| SQLAlchemy model | JPA entity |
| Pydantic schema | Request/response DTO |
| Alembic | Flyway or Liquibase |
| FastAPI dependency | Dependency provisioning or scoped infrastructure |

## Running locally

The application expects PostgreSQL on `localhost:5432`, with a database named `subscriptions` and the development credentials configured in `app/db/database.py` and `alembic.ini`.

Install dependencies from the lockfile:

```shell
uv sync
```

Apply database migrations:

```shell
uv run alembic upgrade head
```

Start the development server:

```shell
uv run fastapi dev app/main.py
```

The interactive API documentation is available at:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Existing endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/v1/plans` | Create a subscription plan |
| `GET` | `/api/v1/plans` | List subscription plans |

## Development principles

- Version public endpoints under `/api/v1`.
- Keep API DTOs separate from persistence entities.
- Maintain explicit router, service, and repository boundaries.
- Evolve the database with migrations instead of runtime schema generation.
- Use typed Python throughout the application.
- Provision request-scoped infrastructure with FastAPI dependencies.
- Keep transaction boundaries explicit in the service layer.
- Prefer a production-oriented package structure as the project grows.
