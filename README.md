# Timetable API

Backend-сервис для формирования расписаний приёма лекарств.

Проект реализован на Python с использованием FastAPI и предназначен для мобильного приложения, которое напоминает пользователям о необходимости приёма лекарств.

## Стек

* Python 3.12+
* FastAPI
* SQLAlchemy 2.0 (async)
* PostgreSQL
* Alembic
* Pydantic Settings
* Pytest
* Ruff
* Mypy

## Реализованные требования

Сервис поддерживает:

* создание расписания приёма лекарств;
* получение списка расписаний пользователя;
* получение расписания с рассчитанными временными метками;
* получение ближайших приёмов лекарств.

Основные правила расчёта:

* приём лекарств возможен только в дневной период:

  * начало: `08:00`
  * конец: `22:00`

* количество приёмов:

  * от 1 раза в день;
  * до ежечасного приёма.

* продолжительность лечения:

  * ограниченный период через `treatment_days`;
  * постоянный приём через `treatment_days=null`.

* все рассчитанные минуты округляются до ближайшего значения, кратного 15 минутам.

Авторизация и аутентификация отсутствуют согласно требованиям тестового задания.

---

# Структура проекта

```
timetable-api
├── app
│   ├── api          # HTTP endpoints
│   ├── core         # настройки приложения
│   ├── db           # подключение к БД
│   ├── models       # SQLAlchemy модели
│   ├── schemas      # Pydantic схемы
│   ├── services     # бизнес-логика
│   └── main.py
│
├── alembic          # миграции базы данных
├── tests            # автоматические тесты
├── pyproject.toml
└── README.md
```

---

# Установка

## Требования

* Python 3.12+
* PostgreSQL 14+

## Клонирование

```bash
git clone https://github.com/aliensen36/timetable-api.git

cd timetable-api
```

## Установка зависимостей

Создание виртуального окружения:

```bash
python -m venv .venv
```

Активация:

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Установка зависимостей:

```bash
pip install -e ".[dev]"
```

---

# Настройка окружения

Создать файл `.env`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/DB
NEXT_TAKINGS_PERIOD_MINUTES=60
```

Параметры:

| Переменная                  | Описание                        | Значение по умолчанию |
| --------------------------- | ------------------------------- | --------------------- |
| DATABASE_URL                | строка подключения PostgreSQL   | -                     |
| NEXT_TAKINGS_PERIOD_MINUTES | период поиска ближайших приёмов | 60 минут              |

---

# Миграции базы данных

Применить миграции:

```bash
alembic upgrade head
```

Создание новой миграции:

```bash
alembic revision --autogenerate -m "migration name"
```

---

# Запуск приложения

Запуск FastAPI:

```bash
uvicorn app.main:app --reload
```

После запуска API доступно:

```
http://127.0.0.1:8000
```

Swagger документация:

```
http://127.0.0.1:8000/docs
```

---

# API

## Health check

### GET `/health`

Ответ:

```json
{
  "status": "ok"
}
```

---

## Создание расписания

### POST `/schedule`

Пример запроса:

```json
{
  "user_id": "animal-123",
  "medicine_name": "Vitamin C",
  "frequency": 3,
  "treatment_days": 14
}
```

Ответ:

```json
{
  "id": "4f3b6c9a-6d7e-4c8e-b5c4-3b9f5d1d1234"
}
```

---

## Получение списка расписаний пользователя

### GET `/schedules?user_id=animal-123`

Ответ:

```json
{
  "schedule_ids": [
    "4f3b6c9a-6d7e-4c8e-b5c4-3b9f5d1d1234"
  ]
}
```

---

## Получение расписания с расчётом времени

### GET `/schedule`

Параметры:

```
user_id
schedule_id
```

Пример ответа:

```json
{
  "id": "4f3b6c9a-6d7e-4c8e-b5c4-3b9f5d1d1234",
  "user_id": "animal-123",
  "medicine_name": "Vitamin C",
  "frequency": 3,
  "treatment_days": 14,
  "daily_schedule": [
    "08:00",
    "15:00",
    "22:00"
  ]
}
```

---

## Ближайшие приёмы

### GET `/next_takings?user_id=animal-123`

Возвращает лекарства, которые необходимо принять в течение периода из настройки:

```env
NEXT_TAKINGS_PERIOD_MINUTES=60
```

Пример ответа:

```json
[
  {
    "schedule_id": "4f3b6c9a-6d7e-4c8e-b5c4-3b9f5d1d1234",
    "medicine_name": "Vitamin C",
    "taking_time": "08:00"
  }
]
```

---

# Тестирование

Запуск тестов:

```bash
pytest
```

Проверяется:

* работа API;
* Pydantic-схемы;
* модели SQLAlchemy;
* настройки приложения;
* расчёт расписания;
* правила округления времени;
* Alembic-конфигурация.

---

# Архитектура

Проект разделён на слои:

* `api` — HTTP слой;
* `schemas` — входные и выходные модели;
* `services` — бизнес-логика;
* `models` — модели базы данных;
* `db` — работа с PostgreSQL.

Бизнес-логика расчёта расписания вынесена отдельно в сервис `schedule_calculator`, что позволяет тестировать её независимо от API и базы данных.

---

# Лицензия

Учебный проект.
