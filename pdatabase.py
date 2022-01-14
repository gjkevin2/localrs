# coding:utf-8


class DatabaseControl(object):
    """wrap SQL in python"""
    def __init__(self, connector, table=None):
        self.conn = connector
        self.cursor = connector.cursor()
        self.table = table
        # self.appid=appid
        # self.appsecret=appsecret

    def CreateTable(self):
        sql = 'CREATE TABLE IF NOT EXISTS ' + self.table + ' (title VARCHAR(255),date VARCHAR(255),href VARCHAR(255),description VARCHAR(255),timestamp VARCHAR(255));'
        self.cursor.execute(sql)

    def InsertData(self, title, date, href, description, timestamp):
        sql = 'INSERT INTO {}(title,date,href,description,timestamp) VALUES(?,?,?,?,?)'.format(
            self.table)
        # print(sql)
        self.cursor.execute(sql, (title, date, href, description, timestamp))
        self.conn.commit()

    def CheckData(self, title):
        sql = 'SELECT * FROM {} where title=?'.format(self.table)
        self.cursor.execute(sql, (title, ))  # 数据库中的title值有引号存在，故用接口进行转义
        result = self.cursor.fetchall()
        return result

    def GetItems(self, date):
        sql = 'SELECT * FROM {} where date=?'.format(self.table)
        self.cursor.execute(sql, (date, ))
        result = self.cursor.fetchall()
        return result

    def DelData(self, timestamp):
        sql = 'DELETE FROM {} where timestamp<{};'.format(
            self.table, timestamp)
        self.cursor.execute(sql)
        self.conn.commit()