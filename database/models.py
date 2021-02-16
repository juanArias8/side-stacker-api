from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .config import Base


class Room(Base):
    __tablename__ = "rooms"
    code = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    user_1 = Column(String)
    user_2 = Column(String)
    winner = Column(String)

    boards = relationship("Board", back_populates="room")


class Board(Base):
    __tablename__ = "boards"
    index = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_code = Column(Integer, ForeignKey("rooms.code"))
    index_i = Column(Integer)
    index_j = Column(Integer)
    value = Column(String)

    room = relationship("Room", back_populates="boards")
