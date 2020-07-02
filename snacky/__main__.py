from snacky.server import Server
import os
import cherrypy
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Snacky')
    parser.add_argument('--port', type=int, required=True, help='Port to run snacky')

    parser.add_argument('--mode',
                        help='Chosen algorithm to pick the best move',
                        choices=["ml", "score", "move", None])

    parser.add_argument('--save',
                        help='Save the game states to a sql lite database',
                        action="store_true")

    args = parser.parse_args()

    server = Server(mode=args.mode, save=args.save)
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})

    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", args.port)),}
    )
    print("Starting Battlesnake Server...")

    cherrypy.quickstart(server)
