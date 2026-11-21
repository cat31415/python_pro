import requests


responce = requests.get("https://jsonplaceholder.typicode.com/users")

if responce.status_code == 200:
    users = responce.json()
    for user in users:
        adres = user['address']
        geo = adres['geo']
        if float(geo['lat']) > 0:
            if float(geo['lng']) < 0:
                print(f"usrname: {user['username']}, city: {adres['city']}, geo: {geo}")