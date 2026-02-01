import time

class Room:

    def __init__(self, id, name):
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
        return f"Group(id={self.id}, name={self.name}, students={len(self.students)})"

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
class Teacher:
    def __init__(self, id, name, login, password, subjects):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.subjects = subjects.copy()
        
    def change_password(self, last_password, new_password):
        if self.password == last_password:
            self.password = new_password
        else:
            raise ValueError("Incorrect password")
        
    def add_subject(self, subject):
        if subject not in self.subjects:
            self.subjects.append(subject)

    def remove_subject(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)
        else:
            raise ValueError("Subject not found in teacher's subjects")
    def __str__(self):
        return f"teacher(id={self.id}, name={self.name}, login={self.password}, sabjects={self.subjects})"

        
 
        
#Создать класс Lesson(id, subject, group, room, teacher) mетоды change_room(new_room), change_teacher(new_teacher), str, создать экземпляр класса Lesson
    
class Lesson:
    def __init__(self, id, subject, group, room, teacher, time):
        self.id = id
        self.subject = subject
        self.group = group
        self.room = room
        self.teacher = teacher
        self.time = time

    def change_room(self, new_room):
        self.room = new_room     

    def change_teacher(self, new_teacher):
        self.teacher = new_teacher
    
    def __str__(self):
        return f"Lesson(id={self.id}, subject={self.subject}, group={self.group}, room={self.room}, teacher={self.teacher}, start_time={self.time.start_time}, end_time={self.time.end_time})"

class Schedule:
    def __init__(self, id, group, lessons):
        self.id = id
        self.group = group
        self.lessons = [[] for _ in range(7)]  # 7 days a week
        self.add_lessons(lessons)
    
    def add_lesson(self, lesson):
        self.lessons[lesson.time.day].append(lesson)
        # дома посмотреть как работает sort и lambda
        self.lessons[lesson.time.day].sort(key=lambda x: x.time.start_time)
    
    def add_lessons(self, lessons):
        for lesson in lessons:
            self.add_lesson(lesson)
    # добавить номер комнаты и учителя в расписани(с новой строки) тоесть каждый день недели занимае 3 строчки
    def __str__(self):
        result = f"Schedule(id={self.id}, group={self.group.name})\n"
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        times = ["09:00-10:30", "10:45-12:15", "12:30-14:00", "14:15-15:45", "16:00-17:30", "17:45-19:15"]
        result += "-" * 108 + "\n"
        result += "Time      |"
        for i in range(6):
            result += f"{times[i].center(15)}|"
        result += "\n"
        for i in range(7):
            result += "-" * 108 + "\n"
            result += f"{days[i].ljust(10)}|"
            for j in range(6):
                for lesson in self.lessons[i]:
                    if lesson.time.start_time == times[j].split('-')[0]:
                        result += f"{lesson.subject.name.center(15)}|"
                        break
                else:
                    result += " " * 15 + "|"
            result += "\n"
            result += " " * 10 + "|"
            for j in range(6):
                for lesson in self.lessons[i]:
                    if lesson.time.start_time == times[j].split('-')[0]:
                        result += f"{lesson.teacher.name.center(15)}|"
                        break
            result += "\n"
            result += " " * 10 + "|"
            for j in range(6):
                for lesson in self.lessons[i]:
                    if lesson.time.start_time == times[j].split('-')[0]:
                        result += f"{lesson.teacher.name.center(15)}|"
                        break
                else:
                    result += " " * 15 + "|"
            result += "\n"
        result += "-" * 108 + "\n"
        return result

class Time:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
       


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
room11 = Room(11, "11")
math = Subject(1, "Mathematics")
physics = Subject(2, "Physics")
teacher = Teacher(1, "Mr. Smith", "smith", "teachpass", [math])
time1 = Time(0, "09:00", "10:30")
lesson1 = Lesson(1, math, group1, room11, teacher, time1)
#teacher.remove_subject(physics)  # This will raise a ValueError
schedule = Schedule(1, group1, [lesson1])
print(teacher)
print(schedule)


