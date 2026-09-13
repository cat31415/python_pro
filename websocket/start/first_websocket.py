from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

connections = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    connections.append(websocket)
    try:
        while True: 

            message = await websocket.receive_text()

            for connection in connections:
                await connection.send_text(message)
            #websocket.close()

    except WebSocketDisconnect:

        print("Клиен отключился")
        connections.remove(websocket)


