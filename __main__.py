from server import Battlesnake
import os
import cherrypy
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Snacky')
    parser.add_argument('--port', type=int, required=True, help='Port to run snacky')
    parser.add_argument('--best-move',
                        help='best move algo')

    args = parser.parse_args()

    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})

    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", args.port)),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
