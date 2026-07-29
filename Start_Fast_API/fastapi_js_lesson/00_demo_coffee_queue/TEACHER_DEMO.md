# Демонстрация «Кофейная очередь + простой SQL»

Это продолжение `SQL_lessons/first_lesson.py`. Здесь используются те же
`psycopg2.connect()`, `cursor.execute()`, `fetchall()`, `commit()` и `close()`.
Docker и ORM в этом занятии не нужны.

## Что хранится где

- меню `drinks` пока остаётся Python-списком;
- очередь хранится в одной таблице `coffee_orders` в PostgreSQL;
- браузер работает только с FastAPI и не подключается к PostgreSQL напрямую.

```text
JavaScript → HTTP/JSON → FastAPI → psycopg2 → простой SQL → PostgreSQL
```

## 1. Подготовка базы через pgAdmin

В `main.py` используются те же настройки, что и в `SQL_lessons`:

```python
DB_CONFIG = {
    "dbname": "first",
    "user": "postgres",
    "password": "pass",
    "host": "localhost",
    "port": "5432",
}
```

Если пароль или название базы отличаются, измените их в `DB_CONFIG`.

В pgAdmin:

1. Запустите локальный сервер PostgreSQL.
2. Откройте базу `first`.
3. Выберите **Query Tool**.
4. Откройте `create_coffee_orders_table.sql`.
5. Выполните файл кнопкой **Execute**.
6. Обновите раздел `Schemas → public → Tables`.

Должна появиться одна таблица `coffee_orders`. Такое отдельное название не
конфликтует с таблицей `orders` из других SQL-упражнений.

## 2. Установка и запуск FastAPI

Из папки `00_demo_coffee_queue`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

На Windows:

```powershell
.venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Интерфейс: <http://127.0.0.1:8000>.
Swagger: <http://127.0.0.1:8000/docs>.

## 3. Подключение

Функция открывает новое соединение:

```python
def connect_to_db():
    return psycopg2.connect(**DB_CONFIG)
```

В обычном учебном скрипте можно открыть одно соединение, выполнить команды и
завершить программу. FastAPI работает долго и принимает много запросов, поэтому
в этом демо функция работы с БД открывает соединение перед SQL-запросом и закрывает
его после выполнения.

## 4. SELECT

Когда браузер отправляет `GET /api/orders`, вызывается:

```python
cursor.execute("""
    SELECT id, customer, drink_id, drink_name, price, status
    FROM coffee_orders
    ORDER BY id;
""")
rows = cursor.fetchall()
```

`fetchall()` возвращает список кортежей. Функция `row_to_order()` превращает каждый
кортеж в словарь, а FastAPI превращает словарь в JSON.

## 5. INSERT

После отправки формы FastAPI сначала находит напиток в Python-списке, а затем
выполняет:

```python
cursor.execute(
    """
    INSERT INTO coffee_orders (
        customer, drink_id, drink_name, price, status
    )
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id, customer, drink_id, drink_name, price, status;
    """,
    (customer, drink_id, drink_name, price, "waiting"),
)
row = cursor.fetchone()
connection.commit()
```

Главные мысли:

- `%s` — безопасные места для значений;
- значения передаются отдельным кортежем;
- не нужно собирать SQL через f-строку;
- `RETURNING` сразу возвращает созданный заказ вместе с новым `id`;
- без `commit()` INSERT не будет окончательно сохранён.

## 6. UPDATE

Кнопка «Заказ готов» отправляет `PATCH`. Сервер выполняет:

```python
cursor.execute(
    """
    UPDATE coffee_orders
    SET status = %s
    WHERE id = %s
    RETURNING id, customer, drink_id, drink_name, price, status;
    """,
    ("ready", order_id),
)
```

Если `fetchone()` вернул `None`, строки с таким `id` нет и FastAPI отвечает `404`.

## 7. Что показать ученикам

1. Открыть таблицу `coffee_orders` в pgAdmin — она пустая.
2. Обновить страницу и найти `SELECT` в `main.py`.
3. Создать заказ через интерфейс.
4. Обновить данные таблицы в pgAdmin и увидеть новую строку.
5. Перезапустить Uvicorn и показать, что заказ сохранился.
6. Нажать «Заказ готов» и увидеть изменение `status`.

Не разбирайте весь файл сверху вниз. Для каждого действия идите по цепочке:

```text
кнопка → fetch → маршрут FastAPI → SQL → таблица → JSON → интерфейс
```

## Вопросы классу

- Почему очередь не пропадает после перезапуска FastAPI?
- Зачем после INSERT вызывается `commit()`?
- Чем `fetchone()` отличается от `fetchall()`?
- Почему значения передаются через `%s`, а не через f-строку?
- Что вернёт UPDATE, если заказа с таким `id` нет?
- Почему соединение и cursor нужно закрывать?

## Тесты

```bash
pytest -q
```

В тестах функции работы с PostgreSQL подменяются временным Python-списком. Поэтому
автотесты проверяют HTTP-контракт и не удаляют данные учеников из базы.
