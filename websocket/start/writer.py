from websocket import create_connection
import time
ws = create_connection("ws://localhost:8000/ws")

print(ws.recv())
ind = 0
while True:
    operation = input("Введите мат операцию")
    # ind += 1
    ws.send(f"Прошло {ind} секунд")
    print(f"ответ от сервера {ws.recv()}")

ws.close()

