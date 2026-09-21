from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    while True:
        messege = await websocket.receive_text()

        if messege  == "exit":
            await websocket.close()
        else:
            await websocket.send_text(messege)


            
