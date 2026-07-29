def my_def(hi, cat, dog):
    print(hi, cat, dog)

arr = [1, "Hi", 12.3]

print(*arr, 1)

d = {"hi": "Привет", "cat": "Кот", "dog": "Собака"}

my_def(*d)
