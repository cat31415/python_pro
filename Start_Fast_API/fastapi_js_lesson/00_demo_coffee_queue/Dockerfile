# Берём небольшой готовый образ с Python 3.12.
FROM python:3.12-slim

# Python сразу выводит логи и не создаёт служебные файлы __pycache__.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Устанавливаем PostgreSQL прямо в этот учебный контейнер.
# В обычном проекте базу данных запускают в отдельном контейнере.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends postgresql \
    && rm -rf /var/lib/apt/lists/*

# Все следующие команды выполняются внутри папки /app контейнера.
WORKDIR /app

# Сначала устанавливаем библиотеки. Docker сможет сохранить этот слой в кеше.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код, фронтенд и остальные файлы приложения.
COPY . .
RUN chmod +x docker-entrypoint.sh

# Подсказываем, что приложение работает на порту 8000.
EXPOSE 8000

# Скрипт сначала запускает PostgreSQL, а затем сервер FastAPI.
CMD ["./docker-entrypoint.sh"]
