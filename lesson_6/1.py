# Добавить класс Bag в котором будет словарь items в котором будут храниться предметы и их количество 
# такжеполе максимальное количество предметов и два метода удалить или добавить предмет

class Character:
    def __init__(self, name, health, attack_power, bag):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.bag = bag
        # добавить сюда экземпляр класса Bag
        
    def attack(self, other):
        other.health -= self.attack_power
        print(f"{self.name} attacs {other.name}")

    def heal(self, amount):
        self.health = min(100, self.helth + amount)
            
    def __str__(self):
        return f"Name: {self.name} health: {self.health}  attack power: {self.attack_power} bag: {self.bag}"

class Bag:
    def __init__(self, items = {}, max_items = 10):
        self.items = items
        self.max_items = max_items
        self.curent_item_count = sum(items.values())
    
    def add_item(self, item_name, quantity):
        if self.curent_item_count + quantity <= self.max_items:
            if item_name in self.items:
                self.items[item_name] += quantity
            else:
                self.items[item_name] = quantity
        else: 
            print("Cannot add items, bag is full")

    def __str__(self):
        return f"Items: {self.items} max items: {self.max_items}"

Bob = Character("Bob", 100, 20, Bag(items={"gun": 2}, max_items=15))
Bob.bag.add_item("potion", 10)
Bob.bag.add_item("potion", 7)
print(Bob)
Alice = Character("Alice", 100, 15, Bag())
print(Bob)
print(Alice)
#Bob.bag.add_item("potion", 1)
Alice.attack(Bob)
print(Bob)