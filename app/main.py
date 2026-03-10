from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from routes import auth_routes, call_routes, conversation_routes, message_routes,converstion_particpant_route
from websocket.chat_socket import manager
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"],)


app.include_router(auth_routes.router)
app.include_router(conversation_routes.router)
app.include_router(message_routes.router)
app.include_router(converstion_particpant_route.router)
app.include_router(call_routes.router)


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):

    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            receiver_id = data["receiver_id"]

            await manager.send_message(receiver_id, data)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
