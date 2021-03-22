import psycopg2
import os


class DataBase:

    def __init__(self):
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])
        self.cur = self.conn.cursor()
        self.cur.execute("ROLLBACK")
        self.conn.commit()

    def execute(self, request, params=()):
        if len(params) > 0:
            self.cur.execute(request, params)
        else:
            self.cur.execute(request)
        res = self.cur.fetchall()
        self.conn.commit()
        return res
