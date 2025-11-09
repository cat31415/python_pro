temps = [3, 4, 2, 1, 0, -1, 1, 2, 5, 6,
         7, 8, 6, 5, 3, 2, 1, 0, -2, -3,
         -1, 1, 3, 5, 6, 7, 4, 3, 2]

print(temps)

a = temps[:10]
print(a, "за 10 дней")

# temps[-7:-2:-1]
s = temps[-7:]
print(s, "за 7 дней")

s = temps[::2]
print(s, "через день")


r = temps[::-1]
print(r)