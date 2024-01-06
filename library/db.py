import pymysql
 
class Sql():
    host = port = username = password = database = None
    
    def connect(self):
        self.conn = pymysql.connect(
            host=Sql.host, 
            port=Sql.port,
            user=Sql.username,
            password=Sql.password,
            database=Sql.database
        )
        self.cursor=self.conn.cursor()
 
    def close(self):
        self.cursor.close()
        self.conn.close()
 
    def get_one(self,sql,params=()):
        result=None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result
 
    def get_all(self,sql,params=()):
        list=()
        try:
            self.connect()
            self.cursor.execute(sql,params)
            list=self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list
 
    def insert(self,sql,params=()):
        return self.__edit(sql,params)
 
    def update(self, sql, params=()):
        return self.__edit(sql, params)
 
    def delete(self, sql, params=()):
        return self.__edit(sql, params)
 
    def __edit(self,sql,params):
        count=0
        try:
            self.connect()
            count=self.cursor.execute(sql,params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count