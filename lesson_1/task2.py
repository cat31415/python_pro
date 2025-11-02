
arr = ["Moskow", "Peter", "Kazan", "Sochi", "Novgorod", "Rostov", "Krasnodar", "Vladivostok", "Vladimir", "Samara"]

arr2 = []

for city in arr:
    if len(city) > 5:
        arr2.append(city)

print(arr2)

arr[0], arr[-1] = arr[-1], arr[0]

# Неправильно
# arr[0] = arr[-1]
# arr[-1] = arr[0]

print(arr)

print('-'*10)

# arr.sort(reverse=True)
# print(arr)

arr_sorted = sorted(arr, reverse=True)

for i in range(0, len(arr_sorted), 2):
    print(arr_sorted[i], end=" ")
print()