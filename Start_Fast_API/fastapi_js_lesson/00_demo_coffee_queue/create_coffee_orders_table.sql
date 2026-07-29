-- 1. В pgAdmin откройте базу first.
-- 2. Выберите Query Tool.
-- 3. Выполните этот файл целиком.

CREATE TABLE IF NOT EXISTS coffee_orders (
    id SERIAL PRIMARY KEY,
    customer VARCHAR(30) NOT NULL,
    drink_id INTEGER NOT NULL,
    drink_name VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'waiting'
);

-- Проверка: после создания таблица должна быть пустой.
SELECT * FROM coffee_orders;
