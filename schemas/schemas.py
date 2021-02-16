from typing import List

from pydantic import BaseModel

from utils import matrix


class RoomBase(BaseModel):
    name: str
    user_1: str = None
    user_2: str = None
    next: str = None


class Room(RoomBase):
    winner: str = None
    board: List[List[str]] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if len(self.board) == 0:
            self.board = matrix.create_board(7)

    def validate_winner(self):
        print("validate winner")
        symbol_1, symbol_2 = 'x', 'o'
        transposed: List[List[str]] = matrix.get_transposed_matrix(self.board)
        diagonals: List[List[str]] = matrix.get_diagonals(self.board)
        diagonals_reversed: List[List[str]] = matrix.get_reversed_diagonals(self.board)

        if self.validate_player(symbol_1, transposed, diagonals, diagonals_reversed):
            self.winner = self.user_1

        if self.validate_player(symbol_2, transposed, diagonals, diagonals_reversed):
            self.winner = self.user_2

    def validate_player(self, symbol, transposed, diagonals, diagonals_reversed):
        print(f"validate player {symbol}")
        return matrix.count_sequence(self.board, symbol, 4) \
               or matrix.count_sequence(transposed, symbol, 4) \
               or matrix.count_sequence(diagonals, symbol, 4) \
               or matrix.count_sequence(diagonals_reversed, symbol, 4)

    class config:
        orm_mode = True


class WebsocketResponse(BaseModel):
    type: str
    message: str
    data: Room
