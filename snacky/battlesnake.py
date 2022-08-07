import random
import functools
import logging
from copy import deepcopy
from queue import LifoQueue
from typing import List, Iterator

from snacky.models import (GameState, BodyPoint, Move,
                           Snake, HazardPoint, HeadPoint,
                           Point, FoodPoint, WallPoint,
                           DangerPoint, KillPoint, SafePoint,
                           DEATH, DANGER)


logger = logging.getLogger(__name__)


class Grid:
    def __init__(self, game_state: GameState):
        print(game_state.dict())  # todo remove

        self.game_state = game_state
        self.turn = game_state.turn
        self.height = game_state.board.height  # y
        self.width = game_state.board.width  # x
        self.you = game_state.you
        self.middle = Point(x=self.width // 2, y=self.height // 2)
        self.snakes = []
        self.food = []

        # create the grid
        self.grid: List[List[Point]] = [
            [SafePoint(x=x, y=y) for x in range(self.width)] for y in range(self.height)
        ]

        # add hazard to the grid
        for hazard in game_state.board.hazards:
            self.add_hazard(hazard)

        # add food to the grid
        for food in game_state.board.food:
            self.add_food(food)

        # sort the food in distance closest to head
        self.food.sort(key=lambda x: x.distance(self.you.head))

        # add snakes to the board
        for snake in game_state.board.snakes:
            # add all the snakes
            self.add_snake(snake=snake)

        # sort the snakes in distance closest to head
        self.snakes.sort(key=lambda x: x.head.distance(self.you.head))

    def add_point(self, point: Point) -> None:
        """ Adding a point to the grid and handling out of bounce exceptions
        """
        if point:
            try:
                if self.is_safe(self.get_point(point.x, point.y)):
                    self.grid[point.y][point.x] = point

                else:
                    logger.debug("Trying to overwrite a danger point.")

            except IndexError:
                logging.error("Trying to add a point outside of the grid.")
                raise
        else:
            logging.error("Trying to add point that is not valid.")

    def add_hazard(self, hazard: HazardPoint):
        self.add_point(HazardPoint(x=hazard.x, y=hazard.y))
        self.food.append(hazard)

    def add_food(self, food: FoodPoint):
        self.add_point(FoodPoint(x=food.x, y=food.y))
        self.food.append(food)

    def add_snake(self, snake: Snake) -> None:
        """ Add a full snake to the grid and add the snake object to the snake list
        :param snake: The snake object to add
        """

        # add the head
        if self.you.id == snake.id:
            snake.head.you = True

        self.add_point(snake.head)

        # add the tail
        self.add_point(snake.tail)

        # add the body
        for body_part in snake.body:
            if body_part != snake.head or body_part != snake.tail:
                self.add_point(body_part)

        # adding the snake to the list of snakes
        self.snakes.append(snake)

        # add danger around bigger enemy snakes head or kill box
        if self.you.id != snake.id:
            if self.you.size <= snake.size:
                self.add_points_around(snake.head, point_type=DangerPoint)
            else:
                self.add_points_around(snake.head, point_type=KillPoint)

    def add_points_around(self, point: Point, point_type, dept=0) -> None:
        """ Will add a type of point around a given point

        :param point: The point to surround with heat
        :param point_type: The point type to surround with
        :param dept: Recursively add the heat to points
        """

        for point in self.get_points_around(point):
            self.add_point(point_type(x=point.x, y=point.y))

            if dept > 0:
                # recursively add more surrounding
                self.add_points_around(point=point,
                                       point_type=point_type,
                                       dept=dept - 1)

    def get_point_up(self, point: Point):
        """ Gets the point up to a given point

        :param point: Initial point
        :return: The point up to the initial point
        """
        return self.get_point(**point.get_coordinates_up())

    def get_point_down(self, point: Point):
        """ Gets the point down to a given point

        :param point: Initial point
        :return: The point down to the initial point
        """
        return self.get_point(**point.get_coordinates_down())

    def get_point_right(self, point: Point):
        """ Gets the point right to a given point

        :param point: Initial point
        :return: The point right to the initial point
        """
        return self.get_point(**point.get_coordinates_right())

    def get_point_left(self, point: Point):
        """ Gets the point left to a given point

        :param point: Initial point
        :return: The point left to the initial point
        """
        return self.get_point(**point.get_coordinates_left())

    def get_points_around(self, point: Point) -> list:
        """ Easy way of returning all surrounding points of a given point

        :param point: initial point
        :return: all 4 points around the initial point
        """
        return [self.get_point_up(point),
                self.get_point_down(point),
                self.get_point_right(point),
                self.get_point_left(point)]

    def filter_dangers(self, points: List[Point], exception: Point = None) -> List[Point]:
        """ Filter out the dangerous points from a list of Points

        :param points: List of points to filter
        :param exception: A point that should be exempt from the rule
        :return: Return a list of points that will not kill you
        """
        safe_points = []
        for point in points:
            if self.is_safe(point):
                safe_points.append(point)

        return safe_points

    def is_safe(self, point: Point, exception: Point = None) -> Point:

        return point.heat < DEATH or \
           point.heat < DANGER or \
           point == exception or \
           (self.turn >= 3 and self.you.health < 100 and point == self.you.tail)

    def get_point(self, x: int, y: int):
        """ Helper to get a Point object at a given point

        :param y:
        :param x:
        :return: The point object at that position
        """

        try:
            # return walls for points on the edge of the grid
            if y == -1:
                return WallPoint(x=x, y=y)

            elif x == -1:
                return WallPoint(x=x, y=y)

            elif y == self.height:
                return WallPoint(x=x, y=y)

            elif x == self.width:
                return WallPoint(x=x, y=y)

            else:
                # returns the point at that grid position
                return self.grid[y][x]

        except (IndexError, AttributeError):
            logging.error("Trying to access a point outside the grid")
            return WallPoint(x=x, y=y)

    def find_biggest_enemy_snake(self):
        biggest_snake = None
        biggest_size = -1
        for snake in self.snakes:
            if snake.size > biggest_size and self.you != snake:
                biggest_snake = snake
                biggest_size = snake.size
        return biggest_snake

    def heat_around(self, point: Point):
        total_heat = 0
        for point in self.get_points_around(point):
            total_heat += point.heat

        return total_heat

    def astar(self, start: Point, end: Point):
        # todo: add logic when I move make the snack move (do_move())
        # this will need to keep the game state for each position in the q
        # todo: return the actual path not just true/false

        stack = LifoQueue()

        grid = deepcopy(self)

        stack.put(start)
        start.mark()
        while not stack.empty():

            stack_point = stack.get()

            if stack_point == end:
                return True

            points = [point for point in grid.filter_dangers(grid.get_points_around(stack_point), exception=end)]
            points.sort(key=lambda p: p.distance(end), reverse=True)

            for point in points:
                if not point.marked:
                    stack.put(point)
                    point.mark()
            # debug
            # print(grid)
            # print(stack.queue)
            # print(points)

    def do_move(self, move):
        """

        :param move:
        :return:
        """
        pass

    def spin_and_survive(self):
        print("SPIN TO SURVIVE")
        safe_points_around = self.filter_dangers(self.get_points_around(self.you.head))

        moves = []
        for point in safe_points_around:
            move = Move(move=self.you.head.resolve_direction(point),
                        point=point)
            # edit the score for each possible move
            move.score["heat"] = move.point.heat
            move.score["no_food"] = 30 if isinstance(move.point, FoodPoint) else 0  # we don't want food
            move.score["distance_tail"] = move.point.distance(self.you.tail)
            move.score["path_to_tail"] = -30 if self.astar(start=move.point, end=self.you.tail) else 0

            if self.food:
                distance_food = move.point.distance(self.food[0])  # since we ordered the food this is the closest food
                if self.you.health < distance_food + 5:
                    move.score.pop("no_food")
                    move.score["food"] = distance_food * 100

            moves.append(move)
        sorted_moves = sorted(moves, key=lambda item: item.score.total)

        print("VALID MOVES: ", sorted_moves)

        for move in sorted_moves:
            print("CHOSEN MOVE: ", move)

            return move

    def best_move_score(self):
        print("BEST MOVE SCORE")
        safe_points_around = self.filter_dangers(self.get_points_around(self.you.head))

        # settings
        biggest_enemy_snake = self.find_biggest_enemy_snake()
        food_multiplier = 1 if self.you.size > 10 else 1.5
        kill_multiplier = 1.2
        distance_middle_multiplier = 1.5

        moves = []

        for point in safe_points_around:
            move = Move(move=self.you.head.resolve_direction(point),
                        point=point)
            # edit the score for each possible move
            move.score["heat"] = move.point.heat
            move.score["distance_middle"] = move.point.distance(self.middle) * distance_middle_multiplier
            move.score["move_heat_around"] = self.heat_around(move.point) / 20
            move.score["path_to_tail"] = -25 if self.astar(start=move.point, end=self.you.tail) else 0

            # move.score["path_corner"] = -15 if self.astar(start=move.point, end=Point(0, 0)) else 0

            if self.food:
                distance_food = move.point.distance(self.food[0])
                if self.you.health < distance_food + 5:
                    food_multiplier *= 2

                move.score["food"] = distance_food * food_multiplier

            if biggest_enemy_snake is not None and self.you.size > biggest_enemy_snake.size:
                closest_smaller_snake = self.snakes[1]
                move.score["kill"] = move.point.distance(closest_smaller_snake.head) * kill_multiplier
            moves.append(move)

        sorted_moves = sorted(moves, key=lambda item: item.score.total)

        print("SORTED MOVES: ", sorted_moves)

        for move in sorted_moves:
            print("CHOSEN MOVE: ", move)
            return move

        # default to the best move if no possible path
        if sorted_moves:
            print("LAST RESORT MOVE: ", sorted_moves[0])
            return sorted_moves[0]

        # Dead...

    def best_move(self):
        """ Spaghetti
            Top 42!
        :return:
        """

        safe_points_around = self.filter_dangers(self.get_points_around(self.you.head))

        # sorted moves in order of heat
        sorted_points = sorted(safe_points_around, key=lambda m: point.heat)

        print("POSSIBLE POINTS: ", sorted_points)

        biggest_enemy_snake = self.find_biggest_enemy_snake()

        if biggest_enemy_snake is None or self.you.size <= biggest_enemy_snake.size + 1:
            # if you are not the biggest, go get food
            if self.food:
                closest_food = self.food[0]

                closest_snake_distance = 9999
                closest_snake = None
                for snake in self.snakes:
                    if snake.head.distance(closest_food) < closest_snake_distance:
                        closest_snake_distance = snake.head.distance(closest_food)
                        closest_snake = snake

                # check if im the closest snake
                if closest_snake.id == self.you.id:
                    min_distance_point = 9999
                    best_food_move = None
                    for move in sorted_moves:
                        if move.point.distance(closest_food) < min_distance_point:
                            min_distance_point = move.point.distance(closest_food)
                            best_food_move = move

                    # check if the food move is also a safe move

                    # check if there's a path after that move
                    if self.astar(best_food_move.point, self.you.tail):
                        print("FOOD MOVE: ", best_food_move)
                        return best_food_move
        else:
            # if you are the biggest, go kill
            if self.snakes and len(self.snakes) > 1:
                # check if food is available
                closest_smaller_snake = self.snakes[1]

                min_distance_point = 9999
                best_snake_kill_move = None
                for move in sorted_moves:
                    if move.point.distance(closest_smaller_snake.head) < min_distance_point:
                        min_distance_point = move.point.distance(closest_smaller_snake.head)
                        best_snake_kill_move = move

                if self.astar(best_snake_kill_move.point, self.you.tail):
                    print("KILL MOVE: ", best_snake_kill_move)
                    return best_snake_kill_move

        # if food or kill was not the way to go
        for move in sorted_moves:
            if self.astar(move.point, self.you.tail):
                print("DEFAULT MOVE: ", move)
                return move

        # default to the best move if no possible path
        print("LAST RESORT MOVE: ", next(iter(sorted_moves)))
        return next(iter(sorted_moves))

    def ml(self):
        return self.best_move_score()

    def __str__(self):
        """Return an ASCII art representation of the board"""
        print("x", self.width, "y", self.height)
        header = "╔"
        for x in range(self.width):
            header += f"={x}" + "=" * (2 - len(str(x)))
            if x != self.width - 1:
                header += "╤"

        header += "╗"

        spacer = "╟┄" + "┄┼┄".join(["┄"] * self.width) + "┄╢"

        footer = "╚"

        for x in range(self.width):
            footer += f"={x}" + "=" * (2 - len(str(x)))
            if x != self.width - 1:
                footer += "╧"

        footer += "╝"

        lines = []

        for y in reversed(range(self.height)):
            line = []
            for x in range(self.width):
                p = self.get_point(x, y)
                line.append(str(p))

            lines.append(str(y) + (" " * (2 - len(str(y)))) + " │ ".join(line) + " " + str(y))

        return "\n".join([header, ("\n" + spacer + "\n").join(lines), footer])
