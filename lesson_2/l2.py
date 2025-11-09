data = ["железный человек", "стражи галактики", "доктор стрендж", "детпул", "мстители"]

a = "главный герой"
# s = ["хобиты"]
data.append("хобиты")
data.insert(0, a)
print(data)
for i in range(2, min(5, len(data))):
    print(data[i])
data = data[:2] + data[4:]
print(data)
# data.remove("главный герой")