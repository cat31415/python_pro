class Room:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Subject:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Group:
    def __init__(self, id, name, students=None):
        self.id = id
        self.name = name
        self.students = students or []


class Teacher:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Time:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time


class Lesson:
    def __init__(self, id, subject, group, room, teacher, time):
        self.id = id
        self.subject = subject
        self.group = group
        self.room = room
        self.teacher = teacher
        self.time = time


class Schedule:
    def __init__(self, id, group, lessons):
        self.id = id
        self.group = group
        self.lessons = [[] for _ in range(7)]
        for lesson in lessons:
            self.lessons[lesson.time.day].append(lesson)

    def __str__(self):
        result = f"Schedule(id={self.id}, group={self.group.name})\n"
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        times = [
            "09:00-10:30",
            "10:45-12:15",
            "12:30-14:00",
            "14:15-15:45",
            "16:00-17:30",
            "17:45-19:15"
        ]

        # ← размеры КАК В ТВОЁМ КОДЕ
        result += "-" * 108 + "\n"
        result += "Time      |"
        for t in times:
            result += t.center(15) + "|"
        result += "\n"

        for i in range(7):
            result += "-" * 108 + "\n"

            # 1 строка — предмет
            result += f"{days[i].ljust(10)}|"
            for t in times:
                for lesson in self.lessons[i]:
                    if lesson.time.start_time == t[:5]:
                        result += lesson.subject.name.center(15) + "|"
                        break
                else:
                    result += " " * 15 + "|"
            result += "\n"

            # 2 строка — комната
            result += " " * 10 + "|"
            for t in times:
                for lesson in self.lessons[i]:
                    if lesson.time.start_time == t[:5]:
                        result += lesson.room.name.center(15) + "|"
                        break
                else:
                    result += " " * 15 + "|"
            result += "\n"

            # 3 строка — учитель
            result += " " * 10 + "|"
            for t in times:
                for lesson in self.lessons[i]:
                    if lesson.time.start_time == t[:5]:
                        result += lesson.teacher.name.center(15) + "|"
                        break
                else:
                    result += " " * 15 + "|"
            result += "\n"

        result += "-" * 108
        return result


# ===== TEST =====
group = Group(1, "Group A")

math = Subject(1, "Mathematics")
teacher = Teacher(1, "Mr. Smith")
room301 = Room(301, "301")

time1 = Time(0, "09:00", "10:30")  # Monday
lesson1 = Lesson(1, math, group, room301, teacher, time1)

schedule = Schedule(1, group, [lesson1])
print(schedule)