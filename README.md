# Timetable API

Backend-сервис для создания расписаний приема лекарств.

Сервис позволяет:

* создавать расписание приема препарата;
* получать список расписаний пользователя;
* получать детали расписания с рассчитанными временами приема;
* получать ближайшие приемы лекарств в заданный период.

Проект реализован на **FastAPI**, использует **PostgreSQL**, **SQLAlchemy Async**, **Alembic** и запускается через **Docker**.

---

## Tech Stack

* Python 3.12+
* FastAPI
* Uvicorn
* SQLAlchemy 2 Async
* PostgreSQL
* asyncpg
* Alembic
* Pydantic Settings
* Docker / Docker Compose
* Pytest

---

# Features

## Schedule creation

Создание расписания приема лекарства.

Поддерживается:

* от 1 до 15 приемов в день;
* постоянный прием (`treatment_days = null`);
* ограниченный курс лечения.

---

## Schedule calculation

Время приема рассчитывается автоматически:

* дневной интервал: **08:00 - 22:00**;
* время округляется до ближайших 15 минут;
* максимальная частота — ежечасный прием.

Примеры:

```
frequency = 1

08:00
```

```
frequency = 3

08:00
15:00
22:00
```

```
frequency = 15

08:00
09:00
10:00
...
22:00
```

---

# API Endpoints

## Health check

```
GET /health
```

Ответ:

```json
{
  "status": "ok"
}
```

---

## Create schedule

```
POST /schedule
```

Request:

```json
{
  "user_id": "user-1",
  "medicine_name": "Ibuprofen",
  "frequency": 3,
  "treatment_days": 10
}
```

Response:

```json
{
  "id": "uuid"
}
```

---

## Get user schedules

```
GET /schedules?user_id=user-1
```

Response:

```json
{
  "schedule_ids": [
    "uuid"
  ]
}
```

---

## Get schedule details

```
GET /schedule?user_id=user-1&schedule_id=<uuid>
```

Response:

```json
{
  "id": "uuid",
  "user_id": "user-1",
  "medicine_name": "Ibuprofen",
  "frequency": 3,
  "treatment_days": 10,
  "created_at": "2026-07-16T12:00:00Z",
  "daily_schedule": [
    "08:00",
    "15:00",
    "22:00"
  ]
}
```

---

## Get next takings

```
GET /next_takings?user_id=user-1
```

Возвращает приемы лекарств в ближайшем временном периоде.

Период задается переменной:

```
NEXT_TAKINGS_PERIOD_MINUTES
```

---

# Running with Docker

## Requirements

Установить:

* Docker Desktop
* Docker Compose

Проверка:

```bash
docker --version
docker compose version
```

---

## Environment

Создать файл `.env`:

```env
DATABASE_URL=postgresql+asyncpg://timetable_user:timetable_password@host.docker.internal:5432/timetable

NEXT_TAKINGS_PERIOD_MINUTES=60
```

---

## Build and start

Запуск контейнера:

```bash
docker compose up --build
```

После запуска API доступно:

```
http://localhost:8000
```

Swagger документация:

```
http://localhost:8000/docs
```

---

## Stop application

Остановить контейнер:

```bash
docker compose down
```

---

# Database migrations

Миграции выполняются автоматически при старте контейнера.

Используется:

```bash
alembic upgrade head
```

Команда запускается внутри:

```
entrypoint.sh
```

---

# Local Development

Установка зависимостей:

```bash
pip install .
```

Запуск приложения:

```bash
uvicorn app.main:app --reload
```

---

# Tests

Запуск тестов:

```bash
pytest
```

Проверяются:

* API endpoints;
* модели SQLAlchemy;
* Pydantic schemas;
* расчет расписания;
* конфигурация;
* Alembic.

---

# Project Structure

```
timetable-api
│
├── alembic
│   └── migrations
│
├── app
│   ├── api
│   │   └── schedules.py
│   │
│   ├── core
│   │   └── config.py
│   │
│   ├── db
│   │   ├── session.py
│   │   └── dependencies.py
│   │
│   ├── models
│   │   └── schedule.py
│   │
│   ├── schemas
│   │   └── schedule.py
│   │
│   ├── services
│   │   ├── schedule.py
│   │   └── schedule_calculator.py
│   │
│   └── main.py
│
├── tests
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── pyproject.toml
├── .env.example
└── README.md
```

---

# Docker Configuration

## Dockerfile

Используется образ:

```
python:3.12-slim
```

Контейнер:

* устанавливает зависимости;
* выполняет миграции;
* запускает FastAPI через Uvicorn.

---

## docker-compose.yml

Compose запускает сервис:

```
timetable-api
```

Порт:

```
8000:8000
```

Автоматически:

* собирает Docker image;
* создает контейнер;
* запускает приложение.

---

# License

Test project.
