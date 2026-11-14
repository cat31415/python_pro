import requests

# response = requests.get('https://jsonplaceholder.typicode.com/users')

# if response.status_code == 200:
#     users = response.json()
#     for user in users:
#         # a = user['username']
#         # if a[0].lower() == "s":
#         d = user['address']
#         if "7" in d['zipcode']:
#                 print(f"Name: {user['name']}, username: {user['username']}, zipcode: {d['zipcode']}")


responce = requests.get("https://jsonplaceholder.typicode.com/comments")

if responce.status_code == 200:
    users = responce.json()
    for user in users:
        a = user["name"].split()
        if len(a) == 6:
            print(f"name: {user["name"]}")