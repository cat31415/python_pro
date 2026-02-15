# попробовать импортировать schedule_gen добавить функцию сохранения дневника в тектовый документ функция принимает готовый schedule и сохраняет его в файл вызвать эту функцию через main.py

import os
car_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(car_dir, "meta.txt")


def save_(schedule):
    with open(data_path, "a", encoding="utf-8") as file:
        file.write(str(schedule))
  



