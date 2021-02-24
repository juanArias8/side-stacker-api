from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from database import crud
from database import models
from database.config import SessionLocal
from database.config import engine
from manager.connection_manager import ConnectionManager
from schemas import schemas
from schemas.schemas import Room

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()
manager = ConnectionManager()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True)


@app.get("/")
async def get():
    return {"message": "fast api side stacker up"}


@app.get("/rooms/{room_name}", response_model=schemas.Room)
async def get_rooms(room_name: str):
    return crud.get_room(db=db, room_name=room_name)


@app.get("/rooms", response_model=List[schemas.Room])
async def get_rooms():
    return crud.get_rooms(db=db)


@app.post("/rooms")
async def create_room(room: Room):
    return manager.create_room(room=room)


@app.post("/rooms/join")
async def join_room(room: Room):
    return manager.join_room(room=room)


@app.websocket("/ws/{room}/{user}")
async def websocket_endpoint(websocket: WebSocket, room: str, user: str):
    await manager.connect(websocket, room, user)
    try:
        while True:
            data = await websocket.receive_json()
            room_instance = Room(**data)

            room_instance.validate_winner()
            if room_instance.winner:
                crud.create_room(db, room_instance)

            if room_instance.boot:
                room_instance.make_boot_move()

            room_instance.get_next_player()
            await manager.broadcast_room(room, room_instance)
    except WebSocketDisconnect:
        await manager.disconnect(room, user)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
