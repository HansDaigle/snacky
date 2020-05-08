from server import GameState
from tests import turn_0, turn_5, turn_3


def test_create_board():

    gs = GameState(data=turn_3)
    print(gs)

    best_move = gs.best_move_around()

    print(gs)

    print(best_move)


def test_astar():
    gs = GameState(data=turn_5)

    print(gs)

    print(astar(gs.grid, gs.me.head, gs.me.tail))

    print(gs)

def test_bm():
    gs = GameState(data=turn_3)
    print(gs)

    best_move = gs.best_move()

    print(gs)

    print(best_move)

