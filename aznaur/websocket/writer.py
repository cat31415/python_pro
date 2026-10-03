from websocket import create_connection
ws = create_connection("ws://localhost:8000/ws")


while True:
    a = input()
    ws.send(a)
    print(ws.recv())
    if a == "exit":
        break
