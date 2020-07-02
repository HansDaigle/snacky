import json
import sqlite3


class DB:

    def __init__(self):
        self.conn = sqlite3.connect('battlesnake.db')

        self.c = self.conn.cursor()
        self.tables = ["raw", "metric"]

        self.init()

    def init(self):
        self.c.execute(f'CREATE TABLE IF NOT EXISTS raw (game_state text)')

        # self.c.execute(f'CREATE TABLE IF NOT EXISTS metric (game_state text)')

    def reset(self):
        for table in self.tables:
            self.c.execute(f"DROP TABLE {table}")

            self.init()

    def add_raw_json(self, data: dict):

        # Insert a row of data
        self.c.execute("""INSERT INTO raw
                          (game_state) 
                          VALUES (?);""", [json.dumps(data)])

        # Save (commit) the changes
        self.conn.commit()
