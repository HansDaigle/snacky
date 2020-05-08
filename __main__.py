from server import Battlesnake
import os
import cherrypy

if __name__ == "__main__":

    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "9291")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
