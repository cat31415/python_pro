class Character:
    def __init__(self, name, health, attack_power, ar):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.ar = ar
        # Добавить поле щит

    def attack(self, other):
        other.health -= self.attack_power
        print(f"{self.name} attacs {other.name}")

    #Добавить функцию лечения def heal(self, amount):
    def heal(self, amount):
        self.health = min(100, self.helth + amount)
            
    def __str__(self):
        return f"Name: {self.name} health: {self.health}  attack power: {self.attack_power}"

Bob = Character("Bob", 100, 20)
Alice = Character("Alice", 100, 15)
print(Bob)
print(Alice)

Alice.attack(Bob)
print(Bob)