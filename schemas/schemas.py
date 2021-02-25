import random
from typing import List, Any

from pydantic import BaseModel

from utils import matrix


class Player(BaseModel):
    name: str = None
    websocket: Any = None

    def clear_data(self):
        self.name = None
        self.websocket = None


class Room(BaseModel):
    name: str
    player_1: Player = None
    player_2: Player = None
    next: str = None
    boot: bool = False
    winner: str = None
    board: List[List[str]] = []

    def __init__(self, **data: Any):
        super().__init__(**data)
        if len(self.board) == 0:
            self.board = matrix.create_board(7)

    def get_next_player(self):
        if self.boot:
            self.next = self.player_1.name
        else:
            if self.next == self.player_1.name:
                self.next = self.player_2.name
            else:
                self.next = self.player_1.name

    def validate_winner(self):
        symbol_1, symbol_2 = 'x', 'o'
        transposed: List[List[str]] = matrix.get_transposed_matrix(self.board)
        diagonals: List[List[str]] = matrix.get_diagonals(self.board)
        diagonals_reversed: List[List[str]] = matrix.get_reversed_diagonals(self.board)
        if self.validate_player(symbol_1, transposed, diagonals, diagonals_reversed):
            self.winner = self.player_1.name
        if self.validate_player(symbol_2, transposed, diagonals, diagonals_reversed):
            self.winner = self.player_2.name

    def validate_player(self, symbol, transposed, diagonals, diagonals_reversed):
        return matrix.count_sequence(self.board, symbol, 4) \
               or matrix.count_sequence(transposed, symbol, 4) \
               or matrix.count_sequence(diagonals, symbol, 4) \
               or matrix.count_sequence(diagonals_reversed, symbol, 4)

    def make_boot_move(self):
        random_i, empty_j = matrix.get_random_empty_index(self.board)
        random_sense = random.choice(['l', 'r'])
        self.board[random_i].pop(empty_j)
        if random_sense == 'l':
            self.board[random_i].insert(0, 'o')
        else:
            self.board[random_i].append('o')

    class config:
        orm_mode = True
