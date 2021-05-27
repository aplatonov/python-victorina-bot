import sqlite3
import os

class DBHelper:
    def __init__(self, dbname="db/victorina.sqlite"):
        os.makedirs('db', exist_ok=True)
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS user (user_id integer, first_name text, last_name text, username text)"
        self.conn.execute(stmt)
        self.conn.commit()

    # def add_user(self, item_text):
    #     stmt = "INSERT INTO user (user_id, user_name) VALUES (?)"
    #     args = (item_text, )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()

    def delete_user(self, user_id):
        stmt = "DELETE FROM user WHERE user_id = (?)"
        args = (user_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    # def get_user(self):
    #     stmt = "SELECT description FROM user"
    #     return [x[0] for x in self.conn.execute(stmt)]
