import sqlite3
import os

class DBHelper:
    schemaFilename = 'dbhelper/dbschema.sql'
    questionFilename = 'dbhelper/question_data.sql'

    def __init__(self, dbname='db/victorina.sqlite'):
        os.makedirs('db', exist_ok=True)
        self.dbname = dbname

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dbname)
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

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

    def upsert_user(self, user_id, first_name, last_name, username):
        self.connect()
        stmt = "SELECT count(*) FROM user WHERE user_id=?"
        args = (user_id, )
        rowcount = self.conn.execute(stmt, args).fetchone()
        if rowcount[0] == 0:
            stmt = "INSERT INTO user (first_name, last_name, username, user_id) VALUES (?,?,?,?)"
        else:
            stmt = "UPDATE user SET first_name=?, last_name=?, username=? WHERE user_id=?"

        args = (first_name, last_name, username, user_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.disconnect()

    def get_questions_for_user(self, user_id, cnt):
        self.connect()
        stmt = "SELECT * FROM question ORDER BY RANDOM() LIMIT ?"
        args = (cnt, )
        questions = self.conn.execute(stmt, args).fetchall()
        self.disconnect()
        return questions

    def upsert_user_points(self, user_id, question_id, points):
        self.connect()
        stmt = "SELECT count(*) FROM user_question WHERE user_id=? AND question_id=?"
        args = (user_id, question_id, )
        rowcount = self.conn.execute(stmt, args).fetchone()
        if rowcount[0] == 0:
            stmt = "INSERT INTO user_question (points, user_id, question_id) VALUES (?,?,?)"
        else:
            stmt = "UPDATE user_question SET points=? WHERE user_id=? AND question_id=?"

        args = (points, user_id, question_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.disconnect()

    def get_info(self, user_id):
        self.connect()
        stmt = "SELECT u.user_id, COUNT(uq.question_id), SUM(uq.points) FROM user u " + \
               "LEFT JOIN user_question uq ON u.user_id = uq.user_id " + \
               "WHERE u.user_id = ? " + \
               "GROUP BY u.user_id"
        args = (user_id, )
        row = self.conn.execute(stmt, args).fetchone()
        if row:
            return dict(count=row[1], sum=row[2])
        else:
            return None

    def delete_user(self, user_id):
        self.connect()
        stmt = "DELETE FROM user WHERE user_id = (?)"
        args = (user_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.disconnect()

    def disconnect(self):
        self.conn.close()