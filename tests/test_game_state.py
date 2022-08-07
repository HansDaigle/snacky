from snacky.battlesnake import Grid
from snacky.models import GameState
from tests.conftest import game_turn_bug


def test_create_board():

    gs = Grid(game_state=GameState(**{'game': {'id': '09d1eddd-7524-444e-b55c-6b2777176028', 'ruleset': {'name': 'wrapped', 'version': 'v1.1.14'}, 'map': 'arcade_maze', 'timeout': 500, 'source': 'challenge'}, 'turn': 1, 'board': {'height': 21, 'width': 19, 'food': [{'x': 9, 'y': 11, 'heat': 10, 'marked': False}], 'hazards': [{'x': 0, 'y': 20, 'heat': 50, 'marked': False}, {'x': 2, 'y': 20, 'heat': 50, 'marked': False}, {'x': 3, 'y': 20, 'heat': 50, 'marked': False}, {'x': 4, 'y': 20, 'heat': 50, 'marked': False}, {'x': 5, 'y': 20, 'heat': 50, 'marked': False}, {'x': 6, 'y': 20, 'heat': 50, 'marked': False}, {'x': 7, 'y': 20, 'heat': 50, 'marked': False}, {'x': 8, 'y': 20, 'heat': 50, 'marked': False}, {'x': 9, 'y': 20, 'heat': 50, 'marked': False}, {'x': 10, 'y': 20, 'heat': 50, 'marked': False}, {'x': 11, 'y': 20, 'heat': 50, 'marked': False}, {'x': 12, 'y': 20, 'heat': 50, 'marked': False}, {'x': 13, 'y': 20, 'heat': 50, 'marked': False}, {'x': 14, 'y': 20, 'heat': 50, 'marked': False}, {'x': 15, 'y': 20, 'heat': 50, 'marked': False}, {'x': 16, 'y': 20, 'heat': 50, 'marked': False}, {'x': 18, 'y': 20, 'heat': 50, 'marked': False}, {'x': 0, 'y': 19, 'heat': 50, 'marked': False}, {'x': 9, 'y': 19, 'heat': 50, 'marked': False}, {'x': 18, 'y': 19, 'heat': 50, 'marked': False}, {'x': 0, 'y': 18, 'heat': 50, 'marked': False}, {'x': 2, 'y': 18, 'heat': 50, 'marked': False}, {'x': 3, 'y': 18, 'heat': 50, 'marked': False}, {'x': 5, 'y': 18, 'heat': 50, 'marked': False}, {'x': 6, 'y': 18, 'heat': 50, 'marked': False}, {'x': 7, 'y': 18, 'heat': 50, 'marked': False}, {'x': 9, 'y': 18, 'heat': 50, 'marked': False}, {'x': 11, 'y': 18, 'heat': 50, 'marked': False}, {'x': 12, 'y': 18, 'heat': 50, 'marked': False}, {'x': 13, 'y': 18, 'heat': 50, 'marked': False}, {'x': 15, 'y': 18, 'heat': 50, 'marked': False}, {'x': 16, 'y': 18, 'heat': 50, 'marked': False}, {'x': 18, 'y': 18, 'heat': 50, 'marked': False}, {'x': 0, 'y': 17, 'heat': 50, 'marked': False}, {'x': 18, 'y': 17, 'heat': 50, 'marked': False}, {'x': 0, 'y': 16, 'heat': 50, 'marked': False}, {'x': 2, 'y': 16, 'heat': 50, 'marked': False}, {'x': 3, 'y': 16, 'heat': 50, 'marked': False}, {'x': 5, 'y': 16, 'heat': 50, 'marked': False}, {'x': 7, 'y': 16, 'heat': 50, 'marked': False}, {'x': 8, 'y': 16, 'heat': 50, 'marked': False}, {'x': 9, 'y': 16, 'heat': 50, 'marked': False}, {'x': 10, 'y': 16, 'heat': 50, 'marked': False}, {'x': 11, 'y': 16, 'heat': 50, 'marked': False}, {'x': 13, 'y': 16, 'heat': 50, 'marked': False}, {'x': 15, 'y': 16, 'heat': 50, 'marked': False}, {'x': 16, 'y': 16, 'heat': 50, 'marked': False}, {'x': 18, 'y': 16, 'heat': 50, 'marked': False}, {'x': 0, 'y': 15, 'heat': 50, 'marked': False}, {'x': 5, 'y': 15, 'heat': 50, 'marked': False}, {'x': 9, 'y': 15, 'heat': 50, 'marked': False}, {'x': 13, 'y': 15, 'heat': 50, 'marked': False}, {'x': 18, 'y': 15, 'heat': 50, 'marked': False}, {'x': 0, 'y': 14, 'heat': 50, 'marked': False}, {'x': 3, 'y': 14, 'heat': 50, 'marked': False}, {'x': 5, 'y': 14, 'heat': 50, 'marked': False}, {'x': 6, 'y': 14, 'heat': 50, 'marked': False}, {'x': 7, 'y': 14, 'heat': 50, 'marked': False}, {'x': 9, 'y': 14, 'heat': 50, 'marked': False}, {'x': 11, 'y': 14, 'heat': 50, 'marked': False}, {'x': 12, 'y': 14, 'heat': 50, 'marked': False}, {'x': 13, 'y': 14, 'heat': 50, 'marked': False}, {'x': 15, 'y': 14, 'heat': 50, 'marked': False}, {'x': 18, 'y': 14, 'heat': 50, 'marked': False}, {'x': 0, 'y': 13, 'heat': 50, 'marked': False}, {'x': 3, 'y': 13, 'heat': 50, 'marked': False}, {'x': 5, 'y': 13, 'heat': 50, 'marked': False}, {'x': 13, 'y': 13, 'heat': 50, 'marked': False}, {'x': 15, 'y': 13, 'heat': 50, 'marked': False}, {'x': 18, 'y': 13, 'heat': 50, 'marked': False}, {'x': 0, 'y': 12, 'heat': 50, 'marked': False}, {'x': 1, 'y': 12, 'heat': 50, 'marked': False}, {'x': 2, 'y': 12, 'heat': 50, 'marked': False}, {'x': 3, 'y': 12, 'heat': 50, 'marked': False}, {'x': 5, 'y': 12, 'heat': 50, 'marked': False}, {'x': 7, 'y': 12, 'heat': 50, 'marked': False}, {'x': 9, 'y': 12, 'heat': 50, 'marked': False}, {'x': 11, 'y': 12, 'heat': 50, 'marked': False}, {'x': 13, 'y': 12, 'heat': 50, 'marked': False}, {'x': 15, 'y': 12, 'heat': 50, 'marked': False}, {'x': 16, 'y': 12, 'heat': 50, 'marked': False}, {'x': 17, 'y': 12, 'heat': 50, 'marked': False}, {'x': 18, 'y': 12, 'heat': 50, 'marked': False}, {'x': 7, 'y': 11, 'heat': 50, 'marked': False}, {'x': 11, 'y': 11, 'heat': 50, 'marked': False}, {'x': 0, 'y': 10, 'heat': 50, 'marked': False}, {'x': 1, 'y': 10, 'heat': 50, 'marked': False}, {'x': 2, 'y': 10, 'heat': 50, 'marked': False}, {'x': 3, 'y': 10, 'heat': 50, 'marked': False}, {'x': 5, 'y': 10, 'heat': 50, 'marked': False}, {'x': 7, 'y': 10, 'heat': 50, 'marked': False}, {'x': 9, 'y': 10, 'heat': 50, 'marked': False}, {'x': 11, 'y': 10, 'heat': 50, 'marked': False}, {'x': 13, 'y': 10, 'heat': 50, 'marked': False}, {'x': 15, 'y': 10, 'heat': 50, 'marked': False}, {'x': 16, 'y': 10, 'heat': 50, 'marked': False}, {'x': 17, 'y': 10, 'heat': 50, 'marked': False}, {'x': 18, 'y': 10, 'heat': 50, 'marked': False}, {'x': 0, 'y': 9, 'heat': 50, 'marked': False}, {'x': 3, 'y': 9, 'heat': 50, 'marked': False}, {'x': 5, 'y': 9, 'heat': 50, 'marked': False}, {'x': 13, 'y': 9, 'heat': 50, 'marked': False}, {'x': 15, 'y': 9, 'heat': 50, 'marked': False}, {'x': 18, 'y': 9, 'heat': 50, 'marked': False}, {'x': 0, 'y': 8, 'heat': 50, 'marked': False}, {'x': 3, 'y': 8, 'heat': 50, 'marked': False}, {'x': 5, 'y': 8, 'heat': 50, 'marked': False}, {'x': 7, 'y': 8, 'heat': 50, 'marked': False}, {'x': 8, 'y': 8, 'heat': 50, 'marked': False}, {'x': 9, 'y': 8, 'heat': 50, 'marked': False}, {'x': 10, 'y': 8, 'heat': 50, 'marked': False}, {'x': 11, 'y': 8, 'heat': 50, 'marked': False}, {'x': 13, 'y': 8, 'heat': 50, 'marked': False}, {'x': 15, 'y': 8, 'heat': 50, 'marked': False}, {'x': 18, 'y': 8, 'heat': 50, 'marked': False}, {'x': 0, 'y': 7, 'heat': 50, 'marked': False}, {'x': 9, 'y': 7, 'heat': 50, 'marked': False}, {'x': 18, 'y': 7, 'heat': 50, 'marked': False}, {'x': 0, 'y': 6, 'heat': 50, 'marked': False}, {'x': 2, 'y': 6, 'heat': 50, 'marked': False}, {'x': 3, 'y': 6, 'heat': 50, 'marked': False}, {'x': 5, 'y': 6, 'heat': 50, 'marked': False}, {'x': 6, 'y': 6, 'heat': 50, 'marked': False}, {'x': 7, 'y': 6, 'heat': 50, 'marked': False}, {'x': 9, 'y': 6, 'heat': 50, 'marked': False}, {'x': 11, 'y': 6, 'heat': 50, 'marked': False}, {'x': 12, 'y': 6, 'heat': 50, 'marked': False}, {'x': 13, 'y': 6, 'heat': 50, 'marked': False}, {'x': 15, 'y': 6, 'heat': 50, 'marked': False}, {'x': 16, 'y': 6, 'heat': 50, 'marked': False}, {'x': 18, 'y': 6, 'heat': 50, 'marked': False}, {'x': 0, 'y': 5, 'heat': 50, 'marked': False}, {'x': 3, 'y': 5, 'heat': 50, 'marked': False}, {'x': 15, 'y': 5, 'heat': 50, 'marked': False}, {'x': 18, 'y': 5, 'heat': 50, 'marked': False}, {'x': 0, 'y': 4, 'heat': 50, 'marked': False}, {'x': 1, 'y': 4, 'heat': 50, 'marked': False}, {'x': 3, 'y': 4, 'heat': 50, 'marked': False}, {'x': 5, 'y': 4, 'heat': 50, 'marked': False}, {'x': 7, 'y': 4, 'heat': 50, 'marked': False}, {'x': 8, 'y': 4, 'heat': 50, 'marked': False}, {'x': 9, 'y': 4, 'heat': 50, 'marked': False}, {'x': 10, 'y': 4, 'heat': 50, 'marked': False}, {'x': 11, 'y': 4, 'heat': 50, 'marked': False}, {'x': 13, 'y': 4, 'heat': 50, 'marked': False}, {'x': 15, 'y': 4, 'heat': 50, 'marked': False}, {'x': 17, 'y': 4, 'heat': 50, 'marked': False}, {'x': 18, 'y': 4, 'heat': 50, 'marked': False}, {'x': 0, 'y': 3, 'heat': 50, 'marked': False}, {'x': 5, 'y': 3, 'heat': 50, 'marked': False}, {'x': 9, 'y': 3, 'heat': 50, 'marked': False}, {'x': 13, 'y': 3, 'heat': 50, 'marked': False}, {'x': 18, 'y': 3, 'heat': 50, 'marked': False}, {'x': 0, 'y': 2, 'heat': 50, 'marked': False}, {'x': 2, 'y': 2, 'heat': 50, 'marked': False}, {'x': 3, 'y': 2, 'heat': 50, 'marked': False}, {'x': 4, 'y': 2, 'heat': 50, 'marked': False}, {'x': 5, 'y': 2, 'heat': 50, 'marked': False}, {'x': 6, 'y': 2, 'heat': 50, 'marked': False}, {'x': 7, 'y': 2, 'heat': 50, 'marked': False}, {'x': 9, 'y': 2, 'heat': 50, 'marked': False}, {'x': 11, 'y': 2, 'heat': 50, 'marked': False}, {'x': 12, 'y': 2, 'heat': 50, 'marked': False}, {'x': 13, 'y': 2, 'heat': 50, 'marked': False}, {'x': 14, 'y': 2, 'heat': 50, 'marked': False}, {'x': 15, 'y': 2, 'heat': 50, 'marked': False}, {'x': 16, 'y': 2, 'heat': 50, 'marked': False}, {'x': 18, 'y': 2, 'heat': 50, 'marked': False}, {'x': 0, 'y': 1, 'heat': 50, 'marked': False}, {'x': 18, 'y': 1, 'heat': 50, 'marked': False}, {'x': 0, 'y': 0, 'heat': 50, 'marked': False}, {'x': 2, 'y': 0, 'heat': 50, 'marked': False}, {'x': 3, 'y': 0, 'heat': 50, 'marked': False}, {'x': 4, 'y': 0, 'heat': 50, 'marked': False}, {'x': 5, 'y': 0, 'heat': 50, 'marked': False}, {'x': 6, 'y': 0, 'heat': 50, 'marked': False}, {'x': 7, 'y': 0, 'heat': 50, 'marked': False}, {'x': 8, 'y': 0, 'heat': 50, 'marked': False}, {'x': 9, 'y': 0, 'heat': 50, 'marked': False}, {'x': 10, 'y': 0, 'heat': 50, 'marked': False}, {'x': 11, 'y': 0, 'heat': 50, 'marked': False}, {'x': 12, 'y': 0, 'heat': 50, 'marked': False}, {'x': 13, 'y': 0, 'heat': 50, 'marked': False}, {'x': 14, 'y': 0, 'heat': 50, 'marked': False}, {'x': 15, 'y': 0, 'heat': 50, 'marked': False}, {'x': 16, 'y': 0, 'heat': 50, 'marked': False}, {'x': 18, 'y': 0, 'heat': 50, 'marked': False}], 'snakes': [{'id': 'gs_SmXj4DBqfdv8bCSGrp6g6wrP', 'name': 'snacky', 'health': 99, 'body': [{'x': 14, 'y': 18, 'heat': 50, 'marked': False}, {'x': 14, 'y': 17, 'heat': 50, 'marked': False}, {'x': 14, 'y': 17, 'heat': 50, 'marked': False}], 'latency': '185', 'head': {'x': 14, 'y': 18, 'heat': 50, 'marked': False, 'you': False}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#e80978', 'head': 'pixel', 'tail': 'pixel'}}]}, 'you': {'id': 'gs_SmXj4DBqfdv8bCSGrp6g6wrP', 'name': 'snacky', 'health': 99, 'body': [{'x': 14, 'y': 18, 'heat': 50, 'marked': False}, {'x': 14, 'y': 17, 'heat': 50, 'marked': False}, {'x': 14, 'y': 17, 'heat': 50, 'marked': False}], 'latency': '185', 'head': {'x': 14, 'y': 18, 'heat': 50, 'marked': False, 'you': False}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#e80978', 'head': 'pixel', 'tail': 'pixel'}}}))
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
