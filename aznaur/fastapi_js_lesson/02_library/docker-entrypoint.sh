#!/bin/sh

# Останавливаем скрипт, если какая-либо команда завершилась с ошибкой.
set -e

# Запускаем установленный внутри контейнера сервер PostgreSQL.
service postgresql start

# Задаём учебному пользователю postgres пароль, используемый в main.py.
su postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'pass';\""

# При первом запуске создаём базу coffee. При повторном запуске этот шаг
# пропускается, потому что база уже существует.
if ! su postgres -c "psql -tAc \"SELECT 1 FROM pg_database WHERE datname='coffee'\"" | grep -q 1; then
    su postgres -c "createdb coffee"
fi

# exec передаёт управление Uvicorn, чтобы Docker корректно останавливал сервер.
exec uvicorn main:app --host 0.0.0.0 --port 8000
