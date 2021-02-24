from typing import Dict

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from schemas.schemas import Room


class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def create_room(self, room: Room):
        if self.rooms.get(room.name) is not None:
            raise ValueError("Room already exits")
        self.rooms.update({room.name: room})
        return room

    def join_room(self, room: Room):
        if self.rooms.get(room.name) is None:
            raise ValueError("Room doesn't exists")
        old_room = self.rooms.get(room.name)
        old_room.player_2 = room.player_2
        self.rooms.update({room.name: old_room})
        return self.get_response_room(old_room)

    async def connect(self, websocket: WebSocket, room_name: str, user: str):
        await websocket.accept()
        local_room = self.rooms.get(room_name)
        if local_room.player_1.name == user:
            local_room.player_1.websocket = websocket
        elif local_room.player_2.name == user:
            local_room.player_2.websocket = websocket
        else:
            raise ValueError("User not exits")
        self.rooms.update({room_name: local_room})
        await self.broadcast_room(local_room.name, local_room)

    async def disconnect(self, room_name: str, user: str):
        local_room = self.rooms.get(room_name)
        if local_room.player_1.name == user:
            local_room.player_1.clear_data()
        elif local_room.player_2.name == user:
            local_room.player_2.clear_data()
        else:
            raise ValueError("User not exits")
        self.rooms.update({room_name: local_room})
        await self.broadcast_room(room_name, local_room)

    async def send_personal_message(self, room: Room, websocket: WebSocket):
        await websocket.send_json(room)

    async def broadcast_room(self, room_name, room: Room):
        response_room = self.get_response_room(room)
        for connection in self.get_room_connections(room_name):
            await connection.send_json(jsonable_encoder(response_room))

    def get_response_room(self, room: Room):
        room_copy = Room(**room.__dict__)
        room_copy.player_1.websocket = None
        room_copy.player_2.websocket = None
        return room_copy

    def get_room_connections(self, room_name: str):
        connections = []
        local_room = self.rooms.get(room_name)
        if local_room.player_1.websocket:
            connections.append(local_room.player_1.websocket)

        if local_room.player_2.websocket:
            connections.append(local_room.player_2.websocket)
        return connections
