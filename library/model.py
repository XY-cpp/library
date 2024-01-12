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
    def __init__(self, id):
        info = list(self.get_one("select * from user where id=%s", id))
        self.id = info[0]
        self.username = info[1]
        self.password = info[2]
        self.name = info[3]
        self.phone = info[4]
        self.email = info[5]
        self.admin = info[6]
        self.llt = info[7]

    @staticmethod
    def login(username, password):
        model = Model()
        result = model.get_one(
            "select id from user where username=%s and password=%s",
            (username, password),
        )
        if result is None:
            return 0
        else:
            return result[0]

    def is_admin(self):
        result = self.get_one(
            "select * from user where username=%s and admin=1", self.username
        )
        return result != None


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


class Item(Model):
    def __init__(self, id):
        # print(self.get_one("select * from item where id=%s", id))
        info = list(self.get_one("select * from item where id=%s", id))
        self.id = info[0]
        self.isbn = info[1]
        self.location = info[2]
        self.status = info[3]

    @staticmethod
    def get_id_by_isbn(isbn):
        model = Model()
        info = list(model.get_all("select id from item where isbn=%s", isbn))
        return [item[0] for item in info]
