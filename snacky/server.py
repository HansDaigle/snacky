from snacky.database import DB
from snacky.battlesnake import GameState

import cherrypy


class Server(object):
    def __init__(self, mode=None, save=False):
        self.mode = mode
        self.save = save

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
        """ This function is called everytime your snake is entered into a game.

        :return: How your snake will look like
        """

        data = cherrypy.request.json

        print("Starting a new game")

        return {"color": "#E80978", "headType": "pixel", "tailType": "pixel"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        """ This function is called on every turn of a game. It's how your snake decides where to move.

        :return: The next move to play
        """

        data = cherrypy.request.json

        if self.save:
            # record the game in the database
            db = DB()
            db.add_raw_json(data=data)

        game_state = GameState(data=data)

        print("TURN:", game_state.turn)

        print(game_state)

        # special algo
        if len(game_state.snakes) == 1 or len(game_state.snakes) > 4:
            return {"move": game_state.spin_and_survive()}

        elif self.mode == "score":
            return {"move": game_state.best_move_score()}

        elif self.mode == "move":
            return {"move": game_state.best_move()}

        elif self.mode == "ml":
            return {"move": game_state.ml()}

        else:
            return {"move": game_state.best_move_score()}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        if self.save:
            # record the game in the database
            db = DB()
            db.add_raw_json(data=data)

        print("END")
        return "ok"
