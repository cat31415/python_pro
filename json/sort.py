def s(d):
    return d["name"]
arr = [{"name" : "John", "age": 30}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}]

sorted_arr = sorted(arr, key=s)
print(sorted_arr)