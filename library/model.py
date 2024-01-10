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


class BookInfo(Model):
    def __init__(self, id):
        self.info = list(self.get_one("select * from book_info where id=%s", id))
        self.id = self.info[0]
        self.name = self.info[1]
        self.author = self.info[2]
        self.press = self.info[3]
        self.isbn = self.info[4]
        self.press_time = self.info[5]
        self.number = self.info[6]
        self.manger = self.info[7]

    @staticmethod
    def total_books():
        model = Model()
        return model.get_one("select count(*) from book_info")[0]
