import random
from typing import List, Any


def create_board(size: int) -> List[List[str]]:
    # return [[' ' for _ in range(size)] for _ in range(size)]
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
        for index in range(len(row)):
            counter = counter + 1 if row[index] == symbol else 0
            if counter == amount:
                return True
    return False


def get_random_empty_index(values):
    visited_rows = [-1] * len(values)
    while True:
        random_i = random.randrange(len(values))
        if get_index(visited_rows, random_i) is None:
            empty_j = get_index(values[random_i], ' ')
            if empty_j is not None:
                return random_i, empty_j

            visited_rows[random_i] = random_i
            if check_visited_all_rows(visited_rows):
                raise ValueError('None row have empty value')


def get_index(row_values: List[Any], wanted_value: Any):
    for index, value in enumerate(row_values):
        if value == wanted_value:
            return index
    return None


def check_visited_all_rows(visited_rows: List[int]):
    for index in range(len(visited_rows)):
        if index != visited_rows[index]:
            return False
    return True


if __name__ == '__main__':
    values = [['x', ' ', 'x', 'o', 'x'],
              ['x', ' ', ' ', 'o', 'o'],
              ['x', 'o', 'x', ' ', 'o'],
              ['x', 'x', 'o', ' ', 'o'],
              ['x', ' ', ' ', 'x', 'o']]

    print(check_visited_all_rows([0, 1]))
