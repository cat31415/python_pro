from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_name):

    await websocket.accept()
 
    connections.append(websocket)
    try:
        await websocket.send_text(f'выможете производить простые математичекие операции')
        while True: 

            message = await websocket.receive_text()

            for connection in connections:
                print(f'{user_name}: {message}')
                await connection.send_text(f'{user_name}: {message}')
            #websocket.close()

    except WebSocketDisconnect:

        print("Клиен отключился")
        connections.remove(websocket)


