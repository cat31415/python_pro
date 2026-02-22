# попробовать импортировать schedule_gen добавить функцию сохранения дневника в тектовый документ функция принимает готовый schedule и сохраняет его в файл вызвать эту функцию через main.py

import json
from . import schedule_gen
import os
car_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(car_dir, "meta.txt")

def save_(schedule):
    with open(data_path, "a", encoding="utf-8") as file:
        file.write(str(schedule))
  

class Students_BD:
    def __init__(self):
        cur_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(cur_dir_path, 'data', 'students_bd.json')
        self.data = {}
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open(self.path, 'w') as f:
                json.dump({}, f)
        
    def add_student(self, student):
        if str(student.id) in self.data:
            raise ValueError("Student with this id already exists")
        self.data[student.id] = {
            "name": student.name,
            "login": student.login,
            "password": student.password,
            "group": student.group.name if student.group else None
        }
        self.save()
        
    def remove_student(self, student_id):
        if str(student_id) not in self.data:
            raise ValueError("Student with this id does not exist")
        del self.data[str(student_id)]
        self.save()
    
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

           
class Teacher_BD:
    def __init__(self):
        cur_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(cur_dir_path, 'data', 'teacher.json')
        self.data = {}
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open(self.path, 'w') as f:
                json.dump({}, f)

    def add_teacher(self, teacher):
        if str(teacher.id) in self.data:
            raise ValueError("Teacher with this id already exists")
        print(teacher)
        self.data[teacher.id] = {
            "name": teacher.name,
            "login": teacher.login,
            "password": teacher.password,
            "subjects": []
        }
        for subject in teacher.subjects:
            self.data[teacher.id]["subjects"].append(str(subject.id))
        self.save()

    def remove_teacher(self, teacher_id):
        if str(teacher_id) not in self.data:
            raise ValueError("Teacher with this id does not exist")
        del self.data[str(teacher_id)]
        self.save()

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4) 

class Subjects_BD:
    def __init__(self):
        cur_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(cur_dir_path, 'data', 'subjects.json')
        self.data = {}
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open(self.path, 'w') as f:
                json.dump({}, f)

    def add_subjects(self, subjects):
        if str(subjects.id) in self.data:
            raise ValueError("subjects with this id already exists")
        self.data[subjects.id] = {
            "id" : subjects.id,
            "name": subjects.name,
        }
        self.save()

    def remove_subjects(self, subjects_id):
        if str(subjects_id) not in self.data:
            raise ValueError("Subjects with this id does not exist")
        del self.data[str(subjects_id)]
        self.save()

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4) 


class Group_BD:
    def __init__(self):
        cur_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(cur_dir_path, 'data', 'group.json')
        self.data = {}
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open(self.path, 'w') as f:
                json.dump({}, f)

    def add_group(self, group):
        if str(group.id) in self.data:
            raise ValueError("group with this id already exists")
        self.data[group.id] = {
            "id" : group.id,
            "name": group.name,
            "students": [],
            "schedule" : str(group.schedule.id) if group.schedule else None
        }
        for student in group.students:
            self.data[group.id]["students"].append(str(student.id))
        self.save()

    def remove_group(self, group_id):
        if str(group_id) not in self.data:
            raise ValueError("group with this id does not exist")
        del self.data[str(group_id)]
        self.save()

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4) 
             



 

