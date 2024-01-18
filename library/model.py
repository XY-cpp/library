from pickle import FALSE
import pymysql
from library import app
import datetime


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
    def total():
        model = Model()
        return model.get_one("select count(*) from icp")[0]

    @staticmethod
    def get_id_list():
        model = Model()
        info = model.get_all("select id from icp")
        return [item[0] for item in info]


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


class Item(Model):
    def __init__(self, id):
        info = list(self.get_one("select * from item where id=%s", id))
        self.id = info[0]
        self.isbn = info[1]
        self.location = info[2]
        self.status = info[3]

    def set_status(self, status):
        self.update(
            "update item \
            set status = %s \
            where id = %s",
            (
                status,
                self.id,
            ),
        )

    @staticmethod
    def get_id_list():
        model = Model()
        info = model.get_all("select id from item")
        return [item[0] for item in info]

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


class Borrow(Model):
    def __init__(self, id):
        info = list(self.get_one("select * from borrow where id=%s"), id)
        self.id = info[0]
        self.book_id = info[1]
        self.user_id = info[2]
        self.start = info[3]
        self.end = info[4]

    @staticmethod
    def borrow_id(user_id):
        model = Model()
        info = model.get_all(
            "select book_id \
            from borrow \
            where \
                user_id = %s and \
                end is null;",
            user_id,
        )
        return [item[0] for item in info]

    @staticmethod
    def tle_id(user_id):
        model = Model()
        info = model.get_all(
            "select book_id \
            from borrow \
            where \
                user_id = %s and \
                datediff(now(), start) > 60 and \
                end is null;",
            user_id,
        )
        return [item[0] for item in info]

    @staticmethod
    def borrow(book_id, user_id, start=None, end=None):
        item = Item(book_id)
        model = Model()
        if item.status == 0:
            item.set_status(3)
            model.update(
                "insert into borrow \
                    (book_id,user_id,start,end) \
                values (%s, %s, %s, %s) \
                ",
                (book_id, user_id, start if start else datetime.date.today(), end),
            )
        else:
            return False

    def reserve(book_id, user_id):
        item = Item(book_id)
        model = Model()
        if item.status == 0:
            item.set_status(2)
            model.update(
                "insert into borrow \
                    (book_id,user_id,start) \
                values (%s, %s, %s) \
                ",
                (book_id, user_id, None),
            )
        else:
            return False

    @staticmethod
    def get_status(user_id):
        class Struct:
            def __init__(self, id, name, author, start, end_thred, end, status):
                self.id = id
                self.name = name
                self.author = author
                self.start = start
                self.end_thred = end_thred
                self.end = end
                self.status = status

        model = Model()
        infos = model.get_all(
            "select item.id, icp.name, icp.author,  borrow.start, \
                date_add(borrow.start, interval 60 day), borrow.end, item.status \
            from item \
            join icp on icp.isbn = item.isbn \
            join borrow on item.id = borrow.book_id \
            join user on user.id = borrow.user_id \
            where user.id = %s \
            ",
            user_id,
        )

        results = []
        for info in infos:
            id, name, author, start, end_thred, end, status = list(info)

            if status == 2:
                status = "已预约"
            elif status == 3:
                status = "已借出"

            if start is None:
                start = end_thred = end = "\\"
            else:
                if end is not None:
                    status = "已归还"
                    end = end.strftime("%Y-%m-%d")
                else:
                    if datetime.date.today() > end_thred:
                        status = "已逾期"
                    end = "\\"
                start = start.strftime("%Y-%m-%d")
                end_thred = end_thred.strftime("%Y-%m-%d")

            results.append(Struct(id, name, author, start, end_thred, end, status))

        return results