class Room:
    def __init__(self, id, name,):
        self.id = id
        self.name = name

class Subject:
     def __init__(self, id, name):
        self.id = id
        self.name = name

class Group:
    def __init__(self, id, name, students, schedule):
        self.id = id
        self.name = name
        self.students = students.copy()
        self.schedule = schedule

    def add_student_to_group(self, student):
        if student.group is not None:
            student.group.remove_student_from_group(student)
        student.group = self
        self.students.append(student)

    def remove_student_from_group(self, student):
        if student in self.students:
            self.students.remove(student)
        else:
            raise ValueError("Student not in that group")

    def __str__(self):
        s_strudents = ', '.join([student.name for student in self.students])
        return f"Group(id={self.id}, name={self.name}, students={s_strudents})"

class Student:
    def __init__(self, id, name, login, password, group):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.group = group

    def change_group(self, group):
        group.add_student_to_group(self)

    def change_password(self, last_password, new_password):
        if self.password == last_password:
            self.password = new_password
        else:
            raise ValueError("Incorrect password")
    
    def __str__(self):
        return f"Student(id={self.id}, name={self.name}, login={self.login}, group={self.group.name if self.group else 'None'})"

#Создать класс Teacher(id, name, login, password, subjects) методы change_password(last_password, new_password), add_subject(subject), remove_subject(subject)

student1 = Student(1, "Alice", "alice123", "pass1", None)
student2 = Student(2, "Bob", "bob456", "pass2", None)
student3 = Student(3, "Charlie", "charlie789", "pass3", None)
students = [student1, student2, student3]
group1 = Group(1, "Group A", students, None)
print(group1)
student4 = Student(4, "David", "david101", "pass4", None)
students[0] = student4
group1.students[0] = student4
print(group1)
group1.add_student_to_group(student1)
group2 = Group(2, "Group B", [], None)
student1.change_group(group2)
print(student1)
print(group1)
print(group2)

m = {"key": "value", "number": 42}
print(m["number"])

arr = [1, 2, 3, 4, 5]
print(arr[2])