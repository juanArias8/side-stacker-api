from typing import Dict

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from schemas.schemas import Room, WebsocketResponse, RoomBase


class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    def create_room(self, room: RoomBase):
        if self.rooms.get(room.name) is not None:
            raise ValueError("Room already exits")

        self.rooms.update({room.name: {room.user_1: None}})
        return room

    def join_room(self, room: Room):
        if self.rooms.get(room.name) is None:
            raise ValueError("Room doesn't exists")

        old_room = self.rooms.get(room.name)
        old_room.update({room.user_2: None})
        self.rooms.update({room.name: old_room})
        room.user_1 = list(old_room.keys())[0]
        return room

    async def connect(self, websocket: WebSocket, room: str, number: int, user: str):
        await websocket.accept()
        room_response = Room(name=room)

        if number == 1:
            self.rooms.get(room).update({user: websocket})
            room_response.user_1 = user
            room_response.next = user
        elif number == 2:
            room_response.user_1 = list(self.rooms.get(room).keys())[0]
            self.rooms.get(room).update({user: websocket})
            room_response.user_2 = user
            room_response.next = room_response.user_1

        response = WebsocketResponse(type="CONNECT", message="User connect", data=room_response)
        await self.broadcast_room(room_response.name, response)

    async def disconnect(self, room_name: str, user: str):
        if user not in self.rooms[room_name].keys():
            raise ValueError("User no exits")

        del self.rooms[room_name][user]
        response = WebsocketResponse(type="DISCONNECT", message=f"user {user} disconnected", data=None)
        await self.broadcast_room(room_name, response)

    async def send_personal_message(self, room: Room, websocket: WebSocket):
        response = WebsocketResponse(type="DATA", message="Personal message", data=room)
        await websocket.send_json(response)

    async def broadcast_room(self, room_name, message: WebsocketResponse):
        print(f"broadcast {message}")
        for connection in self.rooms[room_name].values():
            await connection.send_json(jsonable_encoder(message))
