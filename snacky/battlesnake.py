import random
import logging
import math
from copy import deepcopy
from queue import LifoQueue

from snacky.heat import (LOW_DANGER,
                         MEDIUM_DANGER,
                         HIGH_DANGER,
                         SNAKE_BODY,
                         SAFE, SNAKE_TAIL,
                         SNAKE_HEAD, FOOD,
                         KILL,
                         WALL)


"""
Battlesnake utilities
"""

logger = logging.getLogger(__name__)


class Score(dict):

    @property
    def total(self):
        return sum(self.values())

class Move:
    def __init__(self, direction, point):
        self.direction = direction
        self.point = point
        self.score = Score()


class Point:
    """ A point with x and y coordinates
    """

    def __init__(self, x: int, y: int, heat: int = None):
        """
        :param x: height coordinate
        :param y: width coordinate
        :param heat: level of danger assigned to this point
        """
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
    """ A wall representation
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
    """ A low danger point representation
    """
    def __init__(self, x: int, y: int, heat: int = LOW_DANGER):
        super().__init__(x=x, y=y, heat=heat)


class MediumDanger(Safe):
    """ A danger point representation
    """

    def __init__(self, x: int, y: int, heat: int = MEDIUM_DANGER):
        super().__init__(x=x, y=y, heat=heat)


class HighDanger(Point):
    """ A high danger point representation
    """
    def __init__(self, x: int, y: int, heat: int = HIGH_DANGER):
        super().__init__(x=x, y=y, heat=heat)


class SnakePart(Point):
    """ A snake part representation
    """

    def __init__(self, x: int, y: int, heat: int = SNAKE_BODY):
        super().__init__(x=x, y=y, heat=heat)


class SnakeBodyPart(SnakePart):
    """ A body snake part representation
    """
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, heat=SNAKE_BODY)


class SnakeHeadPart(SnakePart):
    """ A snake head representation
    """
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, heat=SNAKE_TAIL)


class SnakeTailPart(SnakePart):
    """ A snake tail representation
    """
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
    def __init__(self, data: dict):
        """ Represent a battlesnake game state, usually used for one turn

        :param data: game state data received before each turn
        """
        self.turn = data["turn"]
        self.height = data["board"]['height']
        self.width = data["board"]['width']
        self.me = Snake(data["you"])
        self.middle = Point(x=self.width // 2, y=self.height // 2)
        self.snakes = []
        self.food = []

        # all around
        self.grid = [[Safe(x=row, y=col) for col in range(self.height)] for row in range(self.width)]

        # add food to the board
        for food in data["board"]["food"]:
            self._add_food(Food(x=food["x"], y=food["y"]))

        # sort the food in order
        self.food.sort(key=lambda x: x.distance(self.me.head))

        # add snakes to the board
        for snake_json in data["board"]["snakes"]:
            # add all the snakes
            self._add_snake(snake=Snake(snake_json=snake_json))

        # sort the snakes in distance
        self.snakes.sort(key=lambda x: x.head.distance(self.me.head))

    def get_point_up(self, point: Point):
        """ Gets the point up to a given point

        :param point: Initial point
        :return: The point up to the initial point
        """
        return self.get_point(Point(point.x, point.y - 1))

    def get_point_down(self, point: Point):
        """ Gets the point down to a given point

        :param point: Initial point
        :return: The point down to the initial point
        """
        return self.get_point(Point(point.x, point.y + 1))

    def get_point_right(self, point: Point):
        """ Gets the point right to a given point

        :param point: Initial point
        :return: The point right to the initial point
        """
        return self.get_point(Point(point.x + 1, point.y))

    def get_point_left(self, point: Point):
        """ Gets the point left to a given point

        :param point: Initial point
        :return: The point left to the initial point
        """
        return self.get_point(Point(point.x - 1, point.y))

    def get_surrounding_moves(self, point: Point) -> list:
        """ Easy way of returning all surrounding points of a given point

        :param point: initial point
        :return: all 4 points around the initial point
        """

        return [Move(direction="up", point=self.get_point_up(point)),
                Move(direction="down", point=self.get_point_down(point)),
                Move(direction="right", point=self.get_point_right(point)),
                Move(direction="left", point=self.get_point_left(point))]

    def get_possible_moves(self, point: Point, exception: Point = None):
        possible_moves = []

        for move in self.get_surrounding_moves(point):
            if isinstance(move.point, Safe) or isinstance(move.point, HighDanger) or (exception and move.point == exception) or (self.turn >= 3 and self.me.health < 100 and move.point == self.me.tail):
                possible_moves.append(move)

        return possible_moves

    def _add_point(self, point: Point) -> None:
        """ Adding a point to the grid and handling out of bounce exceptions
            * Will only overwrite Safe points

        :param point: Point to add
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
        """ Helper to get a Point object at a given point

        :param point: Point to get, the x and y attribute will be used
        :return: The point object at that position
        """

        try:
            # return walls for points on the edge of the grid
            if point.y == -1:
                return Wall(point.x, point.y)

            elif point.x == -1:
                return Wall(point.x, point.y)

            elif point.y == self.width:
                return Wall(point.x, point.y)

            elif point.x == self.height:
                return Wall(point.x, point.y)

            else:
                # returns the point at that grid position
                return self.grid[point.x][point.y]

        except (IndexError, AttributeError):
            logging.error("Trying to access a point outside the grid")
            return Wall(x=point.x, y=point.y)

    def _add_food(self, food: Food) -> None:
        """ Add the food point to the grid and add the food object to the food list

        :param food: The food object to add
        """

        self._add_point(food)
        self.food.append(food)

    def _add_snake(self, snake: Snake) -> None:
        """ Add a full snake to the grid and add the snake object to the snake list
        :param snake: The snake object to add
        """

        # add the head
        self._add_point(snake.head)

        # add the tail
        self._add_point(snake.tail)

        # add the body
        for body_part in snake.body:
            self._add_point(body_part)

        # adding the snake to the list of snakes
        self.snakes.append(snake)

        # add danger around bigger enemy snakes head or kill box
        if self.me.id != snake.id:
            if len(self.me.body) <= len(snake.body):
                self.add_surrounding(snake.head, point_type=HighDanger, dept=1)
            else:
                self.add_surrounding(snake.head, point_type=Kill)

    def add_surrounding(self, point: Point, point_type, dept=0) -> None:
        """ Will add a type of point around a given point

        :param point: The point to surround with heat
        :param point_type: The point type to surround with
        :param dept: Recursively add the heat to points
        """

        for move in self.get_surrounding_moves(point):
            self._add_point(point_type(x=move.point.x, y=move.point.y))

            if dept > 0:
                # recursively add more surrounding
                self.add_surrounding(point=move.point,
                                     point_type=point_type,
                                     dept=dept - 1)

    def find_biggest_enemy_snake(self):
        biggest_snake = None
        biggest_size = -1
        for snake in self.snakes:
            if snake.size > biggest_size and self.me != snake:
                biggest_snake = snake
                biggest_size = snake.size
        return biggest_snake

    def surrounding_heat(self, point: Point):
        # todo use the buildin sourrounding move function
        return self.get_point_up(point).heat + \
               self.get_point_down(point).heat + \
               self.get_point_left(point).heat + \
               self.get_point_right(point).heat

    def astar(self, start: Point, end: Point):
        # todo: add logic when I move make the snack move (do_move())
        # this will need to keep the game state for each position in the q
        # todo: return the actual path not just true/false

        stack = LifoQueue()

        game_state = deepcopy(self)

        stack.put(start)
        start.mark()

        while not stack.empty():

            current_move = stack.get()

            if current_move == end:
                return True

            moves = [move.point for move in game_state.get_possible_moves(current_move, exception=end)]
            moves.sort(key=lambda x: x.distance(end), reverse=True)

            for move in moves:
                if not move.marked:
                    stack.put(move)
                    move.mark()

            # debug
            # print(game_state)
            # print(stack.queue)
            # print(moves)

    def do_move(self, move):
        """

        :param move:
        :return:
        """
        pass

    def spin_and_survive(self):

        moves = self.get_possible_moves(self.me.head)

        for move in moves:

            move.score["distance_tail"] = move.point.distance(self.me.tail)
            move.score["path_to_tail"] = -25 if self.astar(start=move.point, end=self.me.tail) else 0

            if self.food:
                distance_food = move.point.distance(self.food[0])
                if self.me.health < distance_food + 4:
                    move.score["food"] = distance_food * 100

        sorted_moves = sorted(moves, key=lambda item: item.score.total)

        print("VALID MOVES: ", [move.point for move in sorted_moves])

        for move in sorted_moves:
            print("CHOSEN MOVE: ", move.point)

            return move.direction

    def best_move_score(self):
        """ Algorithm that scores each decisions
        """
        moves = {"up": {"move": self.get_point_up(self.me.head), "score": Score()},
                 "down": {"move": self.get_point_down(self.me.head), "score": Score()},
                 "right": {"move": self.get_point_right(self.me.head), "score": Score()},
                 "left": {"move": self.get_point_left(self.me.head), "score": Score()}}

        print("MOVES: ", moves)

        valid_moves = {}

        biggest_enemy_snake = self.find_biggest_enemy_snake()

        food_multiplier = 1 if self.me.size > 10 else 1.5
        kill_multiplier = 1.2
        distance_middle_multiplier = 1.5

        for move_key, move_data in moves.items():
            if isinstance(move_data["move"], Safe) or isinstance(move_data["move"], HighDanger):

                # edit the score
                move_data["score"]["heat"] = move_data["move"].heat
                move_data["score"]["distance_middle"] = move_data["move"].distance(self.middle) * distance_middle_multiplier
                move_data["score"]["move_surrounding_heat"] = self.surrounding_heat(move_data["move"]) / 20

                move_data["score"]["path_to_tail"] = -25 if self.astar(start=move_data["move"], end=self.me.tail) else 0

                # move_data["score"]["path_corner"] = -15 if self.astar(start=move_data["move"], end=Point(0, 0)) else 0

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

        biggest_enemy_snake = self.find_biggest_enemy_snake()

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
                    if best_food_move in same_best_move and self.astar(moves[best_food_move], self.me.tail):
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

                if best_snake_kill_move in same_best_move and self.astar(moves[best_snake_kill_move], self.me.tail):
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

    def ml(self):
        return self.best_move_score()

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
