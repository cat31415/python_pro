warehouse = {
    "яблоки": 50,
    "бананы": 25,
    "груши": 18,
    "апельсины": 40
}

for fruit, quantity in warehouse.items():
    # print(f"{fruit}: {warehouse[fruit]}")
    print(f"{fruit}: {quantity}")

# s = 0
# for quantity in warehouse.values():
#     s += quantity
s = sum(warehouse.values())
print(s)

s = input("Введите название фрукта: ")
if s in warehouse:
    print(f"{s}: {warehouse[s]}")
    count = int(input("Введите количество, которое хотите забрать: "))
    if count <= warehouse[s]:
        warehouse[s] -= count
        print(f"Вы взяли {count} {s}")
        print(f"Остаток {s}: {warehouse[s]}")
    else:
        print("Недостаточно запасов")
else:
    print("Такого фрукта нет на складе")

s = input("Введите новый фрукт: ")
count = int(input("Введите количество: "))
warehouse[s] = count

for fruit, quantity in warehouse.items():
    print(f"{fruit}: {quantity}")


