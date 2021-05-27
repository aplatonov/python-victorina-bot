import sqlite3
import os

class DBHelper:
    schemaFilename = 'dbhelper/dbschema.sql'
    questionFilename = 'dbhelper/question_data.sql'

    def __init__(self, dbname='db/victorina.sqlite'):
        os.makedirs('../db', exist_ok=True)
        self.dbname = dbname

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)

    def setup(self):
        self.connect()
        with open(self.schemaFilename, 'rt') as file:
            schema = file.read()
        self.conn.executescript(schema)
        self.conn.commit()

        stmt = "SELECT count(*) FROM question"
        rowcount = self.conn.execute(stmt).fetchone()
        if rowcount[0] == 0:
            with open(self.questionFilename, 'rt',  encoding="utf-8") as file:
                schema = file.read()
            self.conn.executescript(schema)
            self.conn.commit()

        self.disconnect()

    def add_user(self, item_text):
        stmt = "INSERT INTO user (user_id, user_name) VALUES (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_user(self, user_id):
        self.connect()
        stmt = "DELETE FROM user WHERE user_id = (?)"
        args = (user_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.disconnect()

    # def get_user(self):
    #     stmt = "SELECT description FROM user"
    #     return [x[0] for x in self.conn.execute(stmt)]

    def disconnect(self):
        self.conn.close()