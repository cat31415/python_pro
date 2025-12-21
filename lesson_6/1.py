class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, other):
        other.health -= self.attack_power
        print(f"{self.name} attacs {other.name}")

    def __str__(self):
        return f"Name: {self.name} health: {self.health}  attack power: {self.attack_power}"

Bob = Character("Bob", 100, 20)
Alice = Character("Alice", 120, 15)
print(Bob)
print(Alice)

Alice.attack(Bob)
print(Bob)