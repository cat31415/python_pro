class Character:
    def __init__(self, name, health, attack_power, armor):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.armor = armor
        
        # Добавить поле щит

    def attack(self, other):
        other.armor -= self.attack_power
        print(f"{self.name} attacs {other.name}")
        

    #Добавить функцию лечения def heal(self, amount):
    def __str__(self):
        return f"Name: {self.name} armor: {self.armor}  attack power: {self.attack_power}  health: {self.health}"

Bob = Character("Bob", 100, 20, 10)
Alice = Character("Alice", 120, 15, 0)
print(Bob)
print(Alice)

Alice.attack(Bob)
print(Bob) 