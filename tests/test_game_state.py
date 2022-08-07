from snacky.battlesnake import Grid
from snacky.models import GameState
from tests.conftest import game_turn_bug


def test_create_board():

    gs = Grid(game_state=GameState(**{'game': {'id': 'f35b0fd6-eacd-432e-b110-a9625133a5f6', 'ruleset': {'name': 'standard', 'version': 'v1.1.14'}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 2, 'board': {'height': 11, 'width': 11, 'food': [{'x': 5, 'y': 5, 'heat': 10, 'marked': False}], 'hazards': [], 'snakes': [{'id': 'gs_9S77d6JXWTrvK4gr8FRhxd6c', 'name': 'snacky', 'health': 100, 'body': [{'x': 6, 'y': 0, 'heat': 50, 'marked': False}, {'x': 6, 'y': 1, 'heat': 50, 'marked': False}, {'x': 5, 'y': 1, 'heat': 50, 'marked': False}, {'x': 5, 'y': 1, 'heat': 50, 'marked': False}], 'latency': '110', 'head': {'x': 6, 'y': 0, 'heat': 50, 'marked': False, 'you': False}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#e80978', 'head': 'pixel', 'tail': 'pixel'}}, {'id': 'gs_pYPS8HyV6hthvB4Mk4JRmtxY', 'name': 'Hungry Bot', 'health': 100, 'body': [{'x': 10, 'y': 6, 'heat': 50, 'marked': False}, {'x': 10, 'y': 5, 'heat': 50, 'marked': False}, {'x': 9, 'y': 5, 'heat': 50, 'marked': False}, {'x': 9, 'y': 5, 'heat': 50, 'marked': False}], 'latency': '1', 'head': {'x': 10, 'y': 6, 'heat': 50, 'marked': False, 'you': False}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#00cc00', 'head': 'alligator', 'tail': 'alligator'}}]}, 'you': {'id': 'gs_9S77d6JXWTrvK4gr8FRhxd6c', 'name': 'snacky', 'health': 100, 'body': [{'x': 6, 'y': 0, 'heat': 50, 'marked': False}, {'x': 6, 'y': 1, 'heat': 50, 'marked': False}, {'x': 5, 'y': 1, 'heat': 50, 'marked': False}, {'x': 5, 'y': 1, 'heat': 50, 'marked': False}], 'latency': '110', 'head': {'x': 6, 'y': 0, 'heat': 50, 'marked': False, 'you': False}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#e80978', 'head': 'pixel', 'tail': 'pixel'}}}))
    gs.best_move_score()
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

    path = gs.possible_path(gs.you.head, gs.you.tail)
    assert bool(path)
    print(gs)
    print(path)

    # possible path 2
    gs = GameState(data=turn_path_2)
    print(gs)

    path = gs.possible_path(gs.get_point_up(gs.you.head), gs.you.tail)
    assert bool(path)
    print(gs)
    print(path)

    # no path 1
    gs = GameState(data=turn_no_path)
    print(gs)
    path = gs.possible_path(gs.get_point_left(gs.you.head), end=gs.you.tail)
    assert not bool(path)
    print(gs)
    print(path)


def test_astar():

    # possible path 1
    gs = GameState(data=turn_path_2)
    print(gs)

    path = gs.astar(gs.you.head, gs.you.tail)
    assert bool(path)

    print(gs)
    print(path)

    # no path 1
    gs = GameState(data=turn_no_path)
    print(gs)

    path = gs.astar(gs.you.head, gs.you.tail)
    assert bool(path)
    print(gs)
    print(path)
