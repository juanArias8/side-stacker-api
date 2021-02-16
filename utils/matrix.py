from typing import List


def create_board(size: int) -> List[List[str]]:
    board: List[List[str]] = []
    for index_i in range(size):
        row: List[str] = []
        for index_j in range(size):
            row.append(' ')
        board.append(row)
    return board


def get_reversed_diagonals(values: List[List[str]]) -> List[List[str]]:
    size = len(values)
    diagonals: List[List[str]] = []
    for index in range((-size + 1), size):
        diagonal: List[str] = []
        for i in range(size):
            for j in range(size):
                if i - j == index:
                    diagonal.append(values[i][j])
        diagonals.append(diagonal)
    return diagonals


def get_diagonals(values: List[List[str]]) -> List[List[str]]:
    size = len(values)
    diagonals: List[List[str]] = []
    for index in range((2 * size) - 1):
        diagonal: List[str] = []
        for i in range(size):
            for j in range(size):
                if i + j == index:
                    diagonal.append(values[i][j])
        diagonals.append(diagonal)
    return diagonals


def get_transposed_matrix(values: List[List[str]]) -> List[List[str]]:
    size = len(values)
    return [[values[j][i] for j in range(size)] for i in range(size)]


def count_sequence(values: List[List[str]], symbol: str, amount: int) -> bool:
    for row in values:
        counter = 0
        for index in range(0, len(row)):
            counter = counter + 1 if row[index] == symbol else 0
            if counter == amount:
                print("count sequence true")
                return True
    return False


if __name__ == '__main__':
    values = [[1, 0, 1, 0, 1],
              [1, 0, 0, 0, 0],
              [1, 0, 1, 1, 0],
              [1, 1, 0, 1, 0],
              [1, 1, 0, 1, 0]]
