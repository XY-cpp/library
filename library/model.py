import pymysql
from library import app


class Model:
    def connect(self):
        self.conn = pymysql.connect(
            host=app.config["host"],
            port=app.config["port"],
            user=app.config["username"],
            password=app.config["password"],
            database=app.config["database"],
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    def get_all(self, sql, params=()):
        list = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list

    def update(self, sql, params=()):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count


class User(Model):
    def __init__(self, username):
        self.username = username

    def login(self, password):
        result = self.get_one(
            "select * from user where username=%s and password=%s",
            (self.username, password),
        )
        return result != None

    def is_admin(self):
        result = self.get_one(
            "select * from user where username=%s and admin=1", self.username
        )
        return result != None

    def name(self):
        result = self.get_one("select name from user where username=%s", self.username)
        if result[0] is None:
            return self.username
        else:
            return result[0]


class Icp(Model):
    def __init__(self, id):
        info = list(self.get_one("select * from icp where id=%s", id))
        self.id = info[0]
        self.name = info[1]
        self.author = info[2]
        self.press = info[3]
        self.isbn = info[4]
        self.press_time = info[5]
        self.number = info[6]
        self.manger = info[7]

    @staticmethod
    def total_books():
        model = Model()
        return model.get_one("select count(*) from icp")[0]
