from typing import List

from sqlalchemy.orm import Session

from schemas import schemas
from . import models


def get_room(db: Session, room_name: str):
    return db.query(models.Room).filter(models.Room.name == room_name).first()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()


def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(name=room.name,
                          user_1=room.player_1.name,
                          user_2=room.player_2.name,
                          winner=room.winner)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    create_board(db=db, room_code=db_room.code, board=room.board)
    return db_room


def create_board(db: Session, room_code: int, board: List[List[str]]):
    for row_index, row_value in enumerate(board):
        for column_index, column_value in enumerate(row_value):
            db_board = models.Board(room_code=room_code,
                                    index_i=row_index,
                                    index_j=column_index,
                                    value=column_value)
            db.add(db_board)

    db.commit()
