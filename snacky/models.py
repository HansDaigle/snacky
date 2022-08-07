from __future__ import annotations
import math
from typing import List, Optional

from pydantic import BaseModel


DEATH = 50
DANGER = 30


class Ruleset(BaseModel):
    name: str
    version: str


class Game(BaseModel):
    id: str
    ruleset: Ruleset
    map: str
    timeout: int
    source: str


class Point(BaseModel):
    x: int
    y: int

    heat: Optional[int] = 17
    marked: Optional[bool] = False

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False

    def __repr__(self):
        return f"{self.__class__.__name__}{ self.__dict__}"

    def __eq__(self, other):
        if other:
            return self.x == other.x and self.y == other.y

        return False

    def __lt__(self, other):
        return self.heat < other.heat

    def __gt__(self, other):
        return self.heat > other.heat

    def __str__(self):
        return "M" if self.marked else "."

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def get_coordinates_up(self) -> (int, int):
        return {"x": self.x, "y": self.y + 1}

    def get_coordinates_down(self) -> (int, int):
        return {"x": self.x, "y": self.y - 1}

    def get_coordinates_right(self) -> (int, int):
        return {"x": self.x + 1, "y": self.y}

    def get_coordinates_left(self) -> (int, int):
        return {"x": self.x - 1, "y": self.y}

    def resolve_direction(self, point_toward):
        if self.get_coordinates_up() == {"x": point_toward.x, "y": point_toward.y}:
            return "up"

        elif self.get_coordinates_down() == {"x": point_toward.x, "y": point_toward.y}:
            return "down"

        elif self.get_coordinates_right() == {"x": point_toward.x, "y": point_toward.y}:
            return "right"

        elif self.get_coordinates_left() == {"x": point_toward.x, "y": point_toward.y}:
            return "left"
        else:
            return None


class SafePoint(Point):
    heat = 15


class FoodPoint(Point):
    heat = 10

    def __str__(self):
        return "F"


class KillPoint(Point):
    heat = 5

    def __str__(self):
        return "K"


class DangerPoint(Point):
    heat = DANGER

    def __str__(self):
        return "X"


class HazardPoint(Point):
    heat = DEATH

    def __str__(self):
        return "Z"


class WallPoint(Point):
    heat = DEATH

    def __str__(self):
        return "W"


class BodyPoint(Point):
    heat = DEATH

    def __str__(self):
        return "S"


class HeadPoint(BodyPoint):
    heat = DEATH
    you: Optional[bool] = False

    def __str__(self):
        return "Y" if self.you else "H"


class TailPoint(BodyPoint):
    heat = DEATH

    def __str__(self):
        return "T"


class Customizations(BaseModel):
    color: str
    head: str
    tail: str


class Snake(BaseModel):
    id: str
    name: str
    health: int
    body: List[BodyPoint]
    latency: str
    head: HeadPoint
    length: int
    shout: str
    squad: str
    customizations: Customizations

    @property
    def tail(self):
        return TailPoint(x=self.body[-1].x, y=self.body[-1].y)

    @property
    def size(self):
        return len(self.body)

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id


class Board(BaseModel):
    height: int
    width: int
    food: List[FoodPoint]
    hazards: List[HazardPoint]
    snakes: List[Snake]


class You(Snake):
    pass


class GameState(BaseModel):
    game: Game
    turn: int
    board: Board
    you: You


class Score(dict):

    @property
    def total(self):
        return sum(self.values())


class OutputMove(BaseModel):
    move: str
    shout: Optional[str]


class Move(OutputMove):
    point: Point
    score: Score = Score()

    def __repr__(self):
        return f"{self.move} ({self.point.x}, {self.point.y}) - {self.score.items()} [{self.score.total}]"


class Info(BaseModel):
    apiversion: str
    author: str
    color: str
    head: str
    tail: str
    version: str
