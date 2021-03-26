import psycopg2
import os


class DataBase:

    def __init__(self):
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])
        self.cur = self.conn.cursor()
        self.cur.execute("ROLLBACK")
        self.conn.commit()

        try:
            self.cur.execute('SELECT * FROM users')
        except Exception:
            self.cur.execute("""CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                data VARCHAR,
            )""")
            self.conn.commit()

    def execute(self, request, params=()):
        if len(params) > 0:
            self.cur.execute(request, params)
        else:
            self.cur.execute(request)
        try:
            res = self.cur.fetchall()
        except psycopg2.ProgrammingError:
            res = []
        self.conn.commit()
        return res
