from abc import ABC
import multiprocessing
import sys

from gunicorn.app.base import BaseApplication
from fastapi import FastAPI
from fastapi import status
import uvicorn

from snacky.models import GameState, OutputMove, Info
from snacky.database import DB
from snacky.battlesnake import Grid

app = FastAPI()


@app.get("/",
         responses={
             status.HTTP_200_OK: {"model": Info,
                                  "description": "This function is called everytime your Battlesnake enters a game."},
         }, )
async def root():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake
    """

    return Info(**{
        "apiversion": "1",
        "author": "Snacky",
        "color": "#E80978",
        "head": "pixel",
        "tail": "pixel",
        "version": "2.0.0-beta"
    })


@app.post("/start",
          responses={
              status.HTTP_200_OK: {"model": None,
                                   "description": "This function is called everytime your Battlesnake enters a game."},
          })
def start(data: GameState):
    """
    This function is called everytime your Battlesnake enters a game.
    It's purely for informational purposes, you don't have to make any decisions here.
    """

    print(f"{data.game.id} START")  # todo change for log
    return


@app.post("/move",
          responses={
              status.HTTP_200_OK: {"model": OutputMove,
                                   "description": "This function is called everytime your Battlesnake enters a game."},
          })
def move(data: GameState):
    """
    This function is called on every turn and is how your Battlesnake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """

    save = False
    mode = "score"

    if save:
        # record the game in the database
        db = DB()
        db.add_raw_json(data=data.dict())

    grid: Grid = Grid(game_state=data)

    print("TURN:", grid.turn)

    print(grid)

    # special algo
    if len(grid.snakes) == 1 or len(grid.snakes) > 4:
        return grid.spin_and_survive()

    elif mode == "score":
        return grid.best_move_score()

    elif mode == "move":
        return grid.best_move()

    elif mode == "ml":
        return grid.ml()

    else:
        return grid.best_move_score()


@app.post("/end",
          responses={
              status.HTTP_200_OK: {"model": None,
                                   "description": "This function is called everytime your Battlesnake enters a game."},
          })
def end(data: GameState):
    """
    This function is called when a game your Battlesnake was in has ended.
    It's purely for informational purposes, you don't have to make any decisions here.
    """

    print(f"{data.game.id} END")
    return


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class BattleSnakeApp(BaseApplication, ABC):

    def __init__(self, wsgi_app, options=None):
        self.options = options or {}
        self.application = wsgi_app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}

        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def is_in_trace_mode():
    return bool(sys.gettrace())


if __name__ == "__main__":
    multi_process = True
    host = "127.0.0.1"
    port = 9291

    if multi_process:
        options = {
            'workers': number_of_workers(),
            'worker_class': 'uvicorn.workers.UvicornWorker',
            'bind': f'{host}:{port}',
        }
        BattleSnakeApp(wsgi_app=app, options=options).run()

    else:
        uvicorn.run(
            app="__init__:app",
            host=host,
            port=port,
            debug=is_in_trace_mode(),
            reload=is_in_trace_mode(),
        )
