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
        self.students = []
        self.schedule = schedule

    def add_group(self, group):
        self.groups.append(group)    





class Student:
    def __init__(self, id, name, login, password, group):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.group = group

    def change_group(self, group):
        self.group = group

    def change_password(self, last_password, new_password):
        if self.password == last_password:
            self.password = new_password
            
        
       


