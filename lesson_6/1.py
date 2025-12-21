# Добавить класс Bag в котором будет словарь items в котором будут храниться предметы и их количество 
# такжеполе максимальное количество предметов и два метода удалить или добавить предмет

class Character:
    def __init__(self, name, health, attack_power, ar, bag):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.ar = ar
        self.bag = bag
        # добавить сюда экземпляр класса Bag

    def attack(self, other):
        other.health -= self.attack_power
        print(f"{self.name} attacs {other.name}")

    def heal(self, amount):
        self.health = min(100, self.helth + amount)
            
    def __str__(self):
        return f"Name: {self.name} health: {self.health}  attack power: {self.attack_power}"

Bob = Character("Bob", 100, 20, Bag())
Alice = Character("Alice", 100, 15, Bag())
print(Bob)
print(Alice)
#Bob.bag.add_item("potion", 1)
Alice.attack(Bob)
print(Bob)