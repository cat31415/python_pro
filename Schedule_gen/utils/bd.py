import json
from . import schedule_gen
import os

class Students_BD:
    def __init__(self):
        cur_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(cur_dir_path, 'data', 'students_bd.json')
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open(self.path, 'w') as f:
                json.dump({}, f)
                self.data = {}
        
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
    pass