import requests

response = requests.get('https://jsonplaceholder.typicode.com/users')

if response.status_code == 200:
    users = response.json()
    for user in users:
        print(f"Name: {user['name']}, Email: {user['username']}, Phone: {user['phone']}")
    