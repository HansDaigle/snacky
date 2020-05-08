from server import GameState
from tests import turn_no_path, turn_path, turn_3, turn_no_path_2, turn_path_2


def test_create_board():

    gs = GameState(data=turn_3)
    print(gs)


def test_nest_move_2():
    gs = GameState(data=turn_3)

    print(gs)
    gs.best_move_score()

    print(gs)


def test_path_to_tail():

    # possible path 1
    gs = GameState(data=turn_path)
    print(gs)

    path = gs.possible_path(gs.me.head, gs.me.tail)
    assert bool(path)
    print(gs)
    print(path)

    # possible path 2
    gs = GameState(data=turn_path_2)
    print(gs)

    path = gs.possible_path(gs.get_point_up(gs.me.head), gs.me.tail)
    assert bool(path)
    print(gs)
    print(path)

    # no path 1
    gs = GameState(data=turn_no_path)
    print(gs)
    path = gs.possible_path(gs.get_point_left(gs.me.head), end=gs.me.tail)
    assert not bool(path)
    print(gs)
    print(path)

