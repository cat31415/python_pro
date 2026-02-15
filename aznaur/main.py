from utils.schedule_gen import *
from utils.bd import *

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

math = Subject(1, "Mathematics")
physics = Subject(2, "Physics")
teacher = Teacher(1, "Mr. Smith", "smith", "teachpass", [math])
room101 = Room(101, "101")
time1 = Time(0, "09:00", "10:30")
lesson1 = Lesson(1, math, group1, room101, teacher, time1)
schedule_group1 = Schedule(1, group1, [lesson1])
print(schedule_group1)

#lesson1 = 
#teacher.remove_subject(physics)  # This will raise a ValueError
print(teacher)

save_(schedule_group1)

students_bd = Students_BD()
try:
    students_bd.add_student(student1)
except ValueError as e:
    print(f"Warning: {e}")
    
try:
    students_bd.add_student(student2)
except ValueError as e:
    print(f"Warning: {e}")

try:
    students_bd.add_student(student3)
except ValueError as e:
    print(f"Warning: {e}")
    
try:
    students_bd.remove_student(student2.id)
except ValueError as e:
    print(f"Warning: {e}")


teacher_BD = Teacher_BD()
try:
    teacher_BD.add_teacher(teacher)
except ValueError as e:
    print(f"Warning: {e}")    


