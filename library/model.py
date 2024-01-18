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


    def find_by_isbn(isbn):
        model = Model()
        return model.get_one("select * from icp where icp.isbn = %s;",isbn)

    def update_number(number, isbn):
        model = Model()
        model.update(
            "update icp \
            set icp.number = icp.number + %s\
            where icp.isbn=%s;",
            (
                number,
                isbn
            ),
        )

    def update(mp):
        model = Model()
        model.update(
            "update icp \
            set icp.name = %s, \
                icp.author = %s, \
                icp.press = %s,\
                icp.isbn = %s,\
                icp.press_time = %s, \
                icp.manager = %s \
            where icp.isbn=%s;",
            (
                mp["书名"],
                mp["作者"],
                mp["出版商"],
                mp["ISBN"],
                mp["出版日期"],
                mp["经办人"],
                mp["ISBN"],
            ),
        )
    def insert(mp):
        model = Model()
        model.update(
            "insert into icp (name,author,press,isbn,press_time,number,manager)\
            values(%s,%s,%s,%s,%s,0,%s);",
            (
                mp["书名"],
                mp["作者"],
                mp["出版商"],
                mp["ISBN"],
                mp["出版日期"],
                mp["经办人"]
            )
        )      


class Item(Model):
    def __init__(self, id):
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

    def get_name_by_isbn(isbn):
        model = Model()
        info = list(model.get_all("select icp.name from icp where icp.isbn=%s", isbn))
        return [item[0] for item in info]

    def total_items():
        model = Model()
        return model.get_one("select count(*) from item")[0]

    def update(mp):
        model = Model()
        model.update(
            "update item \
            set item.location = %s, \
                item.status = %s  \
            where item.id = %s ;",
            (
                mp["地点"],
                mp["状态"],
                mp["id"],
            ),
        )
        # 还要对应的修改borrow list
    
    def add(isbn, location):
        model = Model()
        model.update(
            "insert into item (isbn, location, status)\
                values(%s,%s,0);", (isbn, location)
        )