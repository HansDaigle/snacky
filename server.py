import random
import logging
import math

from heat import (LOW_DANGER,
                  MEDIUM_DANGER,
                  HIGH_DANGER,
                  SNAKE_BODY,
                  SAFE, SNAKE_TAIL,
                  SNAKE_HEAD, FOOD,
                  KILL,
                  WALL)

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

logger = logging.getLogger(__name__)


class Score(dict):

    @property
    def total(self):
        return sum(self.values())


class Point:
    """ A point in the matrix representation
    """

    def __init__(self, x: int, y: int, heat: int = None):
        self.x = x
        self.y = y

        # this can be used by a path algorithm
        self.marked = False

        # level of danger of this point
        self.heat: int = heat

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False

    def __repr__(self):
        return f"{self.__class__.__name__}{ self.__dict__}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.heat < other.heat

    def __gt__(self, other):
        return self.heat > other.heat

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)


class Wall(Point):
    """ A safe point representation
    """

    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, heat=WALL)


class Safe(Point):
    """ A safe point representation
    """

    def __init__(self, x: int, y: int, heat: int = SAFE):
        super().__init__(x=x, y=y, heat=heat)


class Food(Safe):
    """ A food representation
    """

    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, heat=FOOD)


class Kill(Safe):
    """ A potential kill point representation
    """

    def __init__(self, x: int, y: int, heat=KILL):
        super().__init__(x=x, y=y, heat=heat)


class LowDanger(Safe):
    def __init__(self, x: int, y: int, heat: int = LOW_DANGER):
        super().__init__(x=x, y=y, heat=heat)


class MediumDanger(Safe):
    """ A danger point representation
    """

    def __init__(self, x: int, y: int, heat: int = MEDIUM_DANGER):
        super().__init__(x=x, y=y, heat=heat)


class HighDanger(Point):
    def __init__(self, x: int, y: int, heat: int = HIGH_DANGER):
        super().__init__(x=x, y=y, heat=heat)


class SnakePart(Point):
    """ A snake body part representation
    """

    def __init__(self, x: int, y: int, heat: int = SNAKE_BODY):
        super().__init__(x=x, y=y, heat=heat)


class SnakeBodyPart(SnakePart):
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, heat=SNAKE_BODY)


class SnakeHeadPart(SnakePart):
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, heat=SNAKE_TAIL)


class SnakeTailPart(SnakePart):
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, heat=SNAKE_HEAD)


class Snake:
    """ A full snake representation
    """

    def __init__(self, snake_json):
        """ Build a snake object from a dict format

        :param snake_json:

             {
                "id":"gs_DX78Q4VWYjSMfbHh4T4dByDM",
                "name":"hansy-snake",
                "health":100,
                "body":[
                   {
                      "x":9,
                      "y":1
                   },
                   {
                      "x":9,
                      "y":1
                   },
                   {
                      "x":9,
                      "y":1
                   }
                ],
                "shout":""
             }


        """
        # generic data
        self.id = snake_json["id"]
        self.name = snake_json["name"]
        self.health = snake_json["health"]

        # snake parts
        self.head = SnakeHeadPart(x=snake_json["body"][0]["x"], y=snake_json["body"][0]["y"])
        self.tail = SnakeTailPart(x=snake_json["body"][-1]["x"], y=snake_json["body"][-1]["y"])
        self.body = [SnakeBodyPart(x=body_part["x"], y=body_part["y"]) for body_part in snake_json["body"][1:-1]]

        self.size = len(self.body) + 2  # adding the head and the tail

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id


class GameState:
    def __init__(self, data):

        self.turn = data["turn"]
        self.height = data["board"]['height']
        self.width = data["board"]['width']
        self.me = Snake(data["you"])
        self.middle = Point(x=self.width // 2, y=self.height // 2)
        self.snakes = []
        self.food = []

        # all around
        self.grid = [[LowDanger(x=row, y=col) if (row == 0 or col == 0 or row == self.height - 1 or col == self.width - 1) else Safe(x=row, y=col) for
                      col in range(self.height)] for row in range(self.width)]

        # 4 corners
        # self.grid = [[LowDanger(x=row, y=col) if (row == 0 and col == 0) or (
        #             row == 0 and col == self.height - 1) or (row == self.width - 1 and col == self.height - 1) or (
        #             row == self.width - 1 and col == 0) else Safe(x=row, y=col) for
        #               col in range(self.height)] for row in range(self.width)]

        # add food to the board
        for food in data["board"]["food"]:
            self.add_food(Food(x=food["x"], y=food["y"]))

        # sort the food in order
        self.food.sort(key=lambda x: x.distance(self.me.head))

        # add snakes to the board
        for snake_json in data["board"]["snakes"]:
            # add all the snakes
            self.add_snake(snake=Snake(snake_json=snake_json))

        # sort the snakes in distance
        self.snakes.sort(key=lambda x: x.head.distance(self.me.head))

    def get_point_up(self, point: Point):
        if point.y == 0:
            return Wall(point.x, point.y - 1)

        return self.get_point(Point(point.x, point.y - 1))

    def get_point_down(self, point: Point):
        if point.y == self.width - 1:
            return Wall(point.x, point.y + 1)

        return self.get_point(Point(point.x, point.y + 1))

    def get_point_right(self, point: Point):
        if point.x == self.height - 1:
            return Wall(point.x + 1, point.y)

        return self.get_point(Point(point.x + 1, point.y))

    def get_point_left(self, point: Point):
        if point.x == 0:
            return Wall(point.x - 1, point.y)

        return self.get_point(Point(point.x - 1, point.y))

    def add_point(self, point: Point):
        """ Adding a point to the grid and handling out of bounce exceptions

            Will only overwrite Food and Safe

        :param point:
        :return:
        """
        if point:
            try:
                if isinstance(self.get_point(point), Safe) or self.get_point(point).heat < point.heat:
                    self.grid[point.x][point.y] = point

                else:
                    logger.debug("Trying to overwrite a point that is not Safe")

            except IndexError:
                logging.error("Trying to add a point outside of the grid")
        else:
            logging.error("Trying to add point that is not valid")

    def get_point(self, point: Point):

        try:
            # returns a copy
            return self.grid[point.x][point.y]

        except (IndexError, AttributeError):
            logging.error("Trying to access a point outside the grid")
            return Wall(x=point.x, y=point.y)

    def add_food(self, food: Food):
        self.add_point(food)

        # adding the food to the list of food
        self.food.append(food)

    def add_snake(self, snake: Snake):

        # add the head
        self.add_point(snake.head)

        # add the tail
        self.add_point(snake.tail)

        # add the body
        for body_part in snake.body:
            self.add_point(body_part)

        # adding the snake to the list of snakes
        self.snakes.append(snake)

        # add danger around bigger enemy snakes head
        if self.me.id != snake.id:
            if len(self.me.body) <= len(snake.body):
                self.add_surrounding(snake.head, surrounding_type=HighDanger, dept=1)
            else:
                self.add_surrounding(snake.head, surrounding_type=Kill)

    def add_surrounding(self, point: Point, surrounding_type, dept=0):

        point_down = self.get_point_down(point)
        self.add_point(surrounding_type(x=point_down.x, y=point_down.y))

        if dept > 0:
            self.add_surrounding(point=point_down,
                                 surrounding_type=surrounding_type,
                                 dept=dept - 1)

        point_right = self.get_point_right(point)
        self.add_point(surrounding_type(x=point_right.x, y=point_right.y))

        if dept > 0:
            self.add_surrounding(point=point_right,
                                 surrounding_type=surrounding_type,
                                 dept=dept - 1)

        point_up = self.get_point_up(point)
        self.add_point(surrounding_type(x=point_up.x, y=point_up.y))

        if dept > 0:
            self.add_surrounding(point=point_up,
                                 surrounding_type=surrounding_type,
                                 dept=dept - 1)

        point_left = self.get_point_left(point)
        self.add_point(surrounding_type(x=point_left.x, y=point_left.y))

        if dept > 0:
            self.add_surrounding(point=point_left,
                                 surrounding_type=surrounding_type,
                                 dept=dept - 1)

    def find_biggest_enemny_snake(self):
        biggest_snake = None
        biggest_size = -1
        for snake in self.snakes:
            if snake.size > biggest_size and self.me != snake:
                biggest_snake = snake
                biggest_size = snake.size
        return biggest_snake

    def best_move_score(self):
        moves = {"up": {"move": self.get_point_up(self.me.head), "score": Score()},
                 "down": {"move": self.get_point_down(self.me.head), "score": Score()},
                 "right": {"move": self.get_point_right(self.me.head), "score": Score()},
                 "left": {"move": self.get_point_left(self.me.head), "score": Score()}}

        print("MOVES: ", moves)

        valid_moves = {}

        biggest_enemy_snake = self.find_biggest_enemny_snake()

        food_multiplier = 1 if self.me.size > 10 else 1.5
        kill_multiplier = 1.2
        distance_middle_multiplier = 2

        for move_key, move_data in moves.items():
            if isinstance(move_data["move"], Safe) or isinstance(move_data["move"], HighDanger):

                # edit the score
                move_data["score"]["heat"] = move_data["move"].heat
                move_data["score"]["distance_middle"] = move_data["move"].distance(self.middle) * distance_middle_multiplier
                move_data["score"]["move_surrounding_heat"] = self.surrounding_heat(move_data["move"]) / 20
                move_data["score"]["path_to_tail"] = -10 if self.possible_path(start=move_data["move"], end=self.me.tail) else 0

                if self.food:
                    distance_food = move_data["move"].distance(self.food[0])
                    if self.me.health < distance_food + 2:
                        food_multiplier *= 2

                    move_data["score"]["food"] = distance_food * food_multiplier

                if biggest_enemy_snake is not None and self.me.size > biggest_enemy_snake.size:
                    closest_smaller_snake = self.snakes[1]
                    move_data["score"]["kill"] = move_data["move"].distance(closest_smaller_snake.head) * kill_multiplier

                valid_moves.update({move_key: move_data})

        sorted_moves = [(k, v["move"], v["score"]) for k, v in
                        sorted(valid_moves.items(), key=lambda item: item[1]["score"].total)]

        print("VALID MOVES: ", sorted_moves)

        for move, point, _ in sorted_moves:
            print("CHOSEN MOVE: ", move)
            return move

        # default to the best move if no possible path
        if sorted_moves:
            print("LAST RESORT MOVE: ", sorted_moves[0][0])
            return sorted_moves[0][0]

        # Dead...

    def surrounding_heat(self, point: Point):
        return self.get_point_up(point).heat + \
               self.get_point_down(point).heat + \
               self.get_point_left(point).heat + \
               self.get_point_right(point).heat

    def best_move(self):
        """ Spaghetti
            Top 42!
        :return:
        """

        moves = {"up": self.get_point_up(self.me.head),
                 "down": self.get_point_down(self.me.head),
                 "right": self.get_point_right(self.me.head),
                 "left": self.get_point_left(self.me.head)}

        # shuffle
        list_moves = list(moves.items())
        random.shuffle(list_moves)
        moves = dict(list_moves)

        # sorted moves in order of heat
        moves = {k: v for k, v in sorted(moves.items(), key=lambda item: item[1])}
        print("POSSIBLE MOVES: ", moves)

        biggest_enemy_snake = self.find_biggest_enemny_snake()

        if biggest_enemy_snake is None or self.me.size <= biggest_enemy_snake.size + 1:
            # if i'm not the biggest + 2 go get food
            if self.food:
                closest_food = self.food[0]

                closest_snake_distance = 9999
                closest_snake = None
                for snake in self.snakes:
                    if snake.head.distance(closest_food) < closest_snake_distance:
                        closest_snake_distance = snake.head.distance(closest_food)
                        closest_snake = snake

                # check if im the closest snake
                if closest_snake.id == self.me.id:
                    min_distance_point = 9999
                    best_food_move = None
                    for k, v in moves.items():
                        if v.distance(closest_food) < min_distance_point:
                            min_distance_point = v.distance(closest_food)
                            best_food_move = k

                    # check if the food move is also a safe move
                    same_best_move = []
                    for k, v in moves.items():
                        if v.heat == moves[next(iter(moves))].heat:
                            same_best_move.append(k)

                    # check if there's a path after that move
                    if best_food_move in same_best_move and self.possible_path(moves[best_food_move]):
                        print("FOOD MOVE: ", best_food_move)
                        return best_food_move
        else:
            # if i'm the biggest go kill
            if self.snakes:
                # check if food is available
                closest_smaller_snake = self.snakes[1]

                min_distance_point = 9999
                best_snake_kill_move = None
                for k, v in moves.items():
                    if v.distance(closest_smaller_snake.head) < min_distance_point:
                        min_distance_point = v.distance(closest_smaller_snake.head)
                        best_snake_kill_move = k

                same_best_move = []
                for k, v in moves.items():
                    if v.heat == moves[next(iter(moves))].heat:
                        same_best_move.append(k)

                if best_snake_kill_move in same_best_move and self.possible_path(moves[best_snake_kill_move]):
                    print("KILL MOVE: ", best_snake_kill_move)
                    return best_snake_kill_move

        # if food or kill was not the way to go
        for key, value in moves.items():
            if isinstance(value, Safe) or isinstance(value, HighDanger):

                marks = self.possible_path(value, self.me.tail)

                if marks:
                    print(f"MARKS - {key} :", marks)
                    print("BEST DEFAULT MOVE: ", key)
                    return key

        # default to the best move if no possible path
        print("LAST RESORT MOVE: ", next(iter(moves)))
        return next(iter(moves))

    def possible_path(self, start: Point, end: Point = None, end_type=SnakeTailPart):

        queue = [start]

        seen = set()
        seen.add((start.x, start.y))
        total_seen = 0

        while queue:

            last_element = queue.pop(0)

            for possible_move in [self.get_point_up(last_element),
                                  self.get_point_down(last_element),
                                  self.get_point_right(last_element),
                                  self.get_point_left(last_element)]:

                total_seen += 1

                if (end and possible_move == end) or (end_type and isinstance(possible_move, end_type)):
                    return total_seen

                if not ((possible_move.x, possible_move.y) in seen) and (isinstance(possible_move, Safe) or isinstance(possible_move, HighDanger)):
                    seen.add((possible_move.x, possible_move.y))

                    possible_move.mark()
                    queue.append(possible_move)

        return 0

    def __str__(self):
        """Return an ASCII art representation of the board"""

        header = "╔"
        for i in range(self.width):
            header += f"={i}" + "=" * (2 - len(str(i)))
            if i != self.width - 1:
                header += "╤"

        header += "╗"
        spacer = "╟┄" + "┄┼┄".join(["┄"] * self.height) + "┄╢"
        footer = "╚" + "╧".join(["==="] * self.width) + "╝"
        lines = []

        for y in range(self.height):
            line = []
            for x in range(self.width):

                point = Point(x=x, y=y)

                if self.get_point(point).marked:
                    line.append("M")
                    continue

                elif isinstance(self.get_point(point), Kill):
                    line.append("K")
                    continue

                elif isinstance(self.get_point(point), Food):
                    line.append("F")
                    continue

                elif isinstance(self.get_point(point), LowDanger):
                    line.append("x")
                    continue

                elif isinstance(self.get_point(point), MediumDanger):
                    line.append("x")
                    continue

                elif isinstance(self.get_point(point), HighDanger):
                    line.append("X")
                    continue

                elif isinstance(self.get_point(point), Safe):
                    line.append(".")
                    continue

                elif isinstance(self.get_point(point), SnakeBodyPart):
                    line.append("S")
                    continue

                elif isinstance(self.get_point(point), SnakeHeadPart):
                    line.append("H")
                    continue

                elif isinstance(self.get_point(point), SnakeTailPart):
                    line.append("T")
                    continue

                else:
                    line.append(" ")

            lines.append("║ " + " │ ".join(line) + " ║")

        return "\n".join([header, ("\n" + spacer + "\n").join(lines), footer])


class Battlesnake(object):
    def __init__(self):
        self.game_state = None

    @cherrypy.expose
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        return "Hi I'm Snacky and I snack all the time"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        """This function is called everytime your snake is entered into a game.

        :return: How your snake will look like
        """
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("Starting a new game")

        return {"color": "#E80978", "headType": "pixel", "tailType": "pixel"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.

        data = cherrypy.request.json
        print("++++++++++++++++")
        print(data)
        print("++++++++++++++++")
        self.game_state = GameState(data=data)

        print("TURN: ", self.game_state.turn)

        print(self.game_state)

        for snake in self.game_state.snakes:
            if snake.name == "Sssevendaysnake":
                best_move = self.game_state.best_move()
                break
        else:
            best_move = self.game_state.best_move_score()

        return {"move": best_move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"
