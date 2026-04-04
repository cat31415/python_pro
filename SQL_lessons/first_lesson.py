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
    ("Олег", 16, 78)
]

cursor.executemany("""
INSERT INTO students (name, age, mark)
VALUES (%s, %s, %s);
""", students)

conn.commit()

cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

# print(rows)

for row in rows:
    print(row)

conn.close()







#import pandas as pd

# df = pd.read_sql("SELECT * FROM students", conn)
# print(df)

# import matplotlib.pyplot as plt

# df['age'].value_counts().plot(kind='bar')
# plt.title("Возраст студентов")
# plt.xlabel("Возраст")
# plt.ylabel("Количество")
# plt.show()