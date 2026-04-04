import psycopg2 
import pandas as pd 
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname="first",
    user="postgres",
    password="pass",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
print("Подключение успешно!")

cursor.execute("DROP TABLE IF EXISTS students")

cursor.execute("""
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INTEGER,
    mark INTEGER
);
""")

conn.commit()

students = [
    ("Иван", 15, 85),
    ("Мария", 14, 90),
    ("Олег", 16, 78),
    ("Игорь", 15, 85),
]

cursor.executemany("""
INSERT INTO students (name, age, mark)
VALUES (%s, %s, %s);
""", students)

conn.commit()

# Получить только фамилию и оценку
cursor.execute('''SELECT name, mark FROM students
               where age > 14
               order by mark
               ''')

rows = cursor.fetchall()

# print(rows)

for row in rows:
    print(row)

df = pd.read_sql("SELECT id, name, mark FROM students", conn)
print(df)


df['mark'].value_counts().plot(kind='bar')
plt.title("Оценки студентов")
plt.xlabel("Оценка")
plt.ylabel("Количество")
plt.show()

conn.close()





