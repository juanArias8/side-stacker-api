from main import get_room_instance_from_data
from utils.matrix import get_random_empty_index

values_winner = [['x', 'x', 'x', 'o', 'x'],
                 ['x', ' ', 'x', 'o', 'o'],
                 ['o', 'o', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'o'],
                 ['x', 'x', ' ', 'x', 'o']]


def test_matrix():
    data = {
        'name': 'room',
        'player_1': {'name': 'player1'},
        'player_2': {'name': 'boot'},
        'next': 'player1',
        'boot': True,
        'winner': None,
        'board': values_winner
    }

    room_instance = get_room_instance_from_data(data)
    assert room_instance.winner == 'player1'
    assert room_instance.board == values_winner


def test_random_empty_index():
    for i in range(10000):
        random_i, empty_j = get_random_empty_index(values_winner)
        assert values_winner[random_i][empty_j] == ' '


if __name__ == '__main__':
    test_matrix()
    test_random_empty_index()
