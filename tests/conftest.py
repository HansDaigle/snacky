from snacky.models import Game, Ruleset, GameState

start_sample = {
    "game": {
        "id": "totally-unique-game-id",
        "ruleset": {
            "name": "standard",
            "version": "v1.2.3"

        },
        "map": "standard",
        "timeout": 500,
        "source": "league"
    },
    "turn": 1,
    "board": {
        "height": 11,
        "width": 11,
        "food": [
            {"x": 5, "y": 5},
            {"x": 9, "y": 0},
            {"x": 2, "y": 6}
        ],
        "hazards": [
            {"x": 0, "y": 0},
            {"x": 0, "y": 1},
            {"x": 0, "y": 2}
        ],
        "snakes": [
            {
                "id": "totally-unique-snake-id",
                "name": "Sneky McSnek Face",
                "health": 54,
                "body": [
                    {"x": 0, "y": 0},
                    {"x": 1, "y": 0},
                    {"x": 2, "y": 0}
                ],
                "latency": "123",
                "head": {"x": 0, "y": 0},
                "length": 3,
                "shout": "why are we shouting??",
                "squad": "1",
                "customizations": {
                    "color": "#26CF04",
                    "head": "smile",
                    "tail": "bolt"
                }
            }
        ]
    },
    "you": {
        "id": "totally-unique-snake-id",
        "name": "Sneky McSnek Face",
        "health": 54,
        "body": [
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 2, "y": 0}
        ],
        "latency": "123",
        "head": {"x": 0, "y": 0},
        "length": 3,
        "shout": "why are we shouting??",
        "squad": "1",
        "customizations": {
            "color": "#26CF04",
            "head": "smile",
            "tail": "bolt"
        }
    }
}

turn_0 = {'game': {'id': '05dd08cc-740d-4786-81a7-64315af22615', 'ruleset': {'name': 'standard', 'version': 'v1.1.14'}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 5, 'board': {'height': 11, 'width': 11, 'food': [{'x': 0, 'y': 4, 'heat': 10, 'marked': False}, {'x': 5, 'y': 5, 'heat': 10, 'marked': False}], 'hazards': [], 'snakes': [{'id': 'gs_ddFPgbbQm3tKGQfq6xHDbwxH', 'name': 'snacky', 'health': 95, 'body': [{'x': 1, 'y': 10, 'heat': 40, 'marked': False}, {'x': 1, 'y': 9, 'heat': 40, 'marked': False}, {'x': 1, 'y': 8, 'heat': 40, 'marked': False}], 'latency': '500', 'head': {'x': 1, 'y': 10, 'heat': 50, 'marked': False}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#e80978', 'head': 'pixel', 'tail': 'pixel'}}]}, 'you': {'id': 'gs_ddFPgbbQm3tKGQfq6xHDbwxH', 'name': 'snacky', 'health': 95, 'body': [{'x': 1, 'y': 10, 'heat': 40, 'marked': False}, {'x': 1, 'y': 9, 'heat': 40, 'marked': False}, {'x': 1, 'y': 8, 'heat': 40, 'marked': False}], 'latency': '500', 'head': {'x': 1, 'y': 10, 'heat': 50, 'marked': False}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#e80978', 'head': 'pixel', 'tail': 'pixel'}}}
game_turn_0 = GameState(**turn_0)

turn_bug = {'game': {'id': '328c6594-0912-4999-99b0-252e16c3f6db', 'ruleset': {'name': 'standard', 'version': 'v1.1.14'}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 5, 'board': {'height': 11, 'width': 11, 'food': [{'x': 0, 'y': 4, 'heat': 10, 'marked': False}, {'x': 5, 'y': 5, 'heat': 10, 'marked': False}], 'hazards': [], 'snakes': [{'id': 'gs_76Cb4cmd9Xdyg8Wp93yKGm4d', 'name': 'snacky', 'health': 95, 'body': [{'x': 1, 'y': 10, 'heat': 40, 'marked': False}, {'x': 1, 'y': 9, 'heat': 40, 'marked': False}, {'x': 1, 'y': 8, 'heat': 40, 'marked': False}], 'latency': '158', 'head': {'x': 1, 'y': 10, 'heat': 50, 'marked': False}, 'length': 3, 'shout': 'Miam!', 'squad': '', 'customizations': {'color': '#e80978', 'head': 'pixel', 'tail': 'pixel'}}]}, 'you': {'id': 'gs_76Cb4cmd9Xdyg8Wp93yKGm4d', 'name': 'snacky', 'health': 95, 'body': [{'x': 1, 'y': 10, 'heat': 40, 'marked': False}, {'x': 1, 'y': 9, 'heat': 40, 'marked': False}, {'x': 1, 'y': 8, 'heat': 40, 'marked': False}], 'latency': '158', 'head': {'x': 1, 'y': 10, 'heat': 50, 'marked': False}, 'length': 3, 'shout': 'Miam!', 'squad': '', 'customizations': {'color': '#e80978', 'head': 'pixel', 'tail': 'pixel'}}}
game_turn_bug = GameState(**turn_bug)
