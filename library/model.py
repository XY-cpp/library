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
