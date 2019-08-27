import sqlite3
import datetime

class database:
    def __init__(self, path):
        self.__connect(path)

    def __del__(self):
        self.__disconnect()

    # 连接数据库
    def __connect(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    # 数据库断开连接
    def __disconnect(self):
        self.cursor.close()
        self.conn.close()

    # 执行SQL语句
    def execute(self, sql):
        return self.cursor.execute(sql)

    # 提交修改
    def commit(self):
        return self.conn.commit()

    # 返回结果
    def fetchall(self):
        return self.cursor.fetchall()

    # 判断表是否存在
    def existTable(self, name):
        self.cursor.execute('select count(*) from sqlite_master where type=\'table\' and name=\'%s\'' % name)
        count = self.cursor.fetchone()[0]
        return True if count != 0 else False

    # 日线转换为周线
    def toWeek(self, data):
        dataw = []
        open = close = high = low = vol = 0.0
        date = None
        enable = False

        for item in data:
            week = datetime.datetime.strptime(item[0], '%Y-%m-%d').weekday()

            if week == 0: 
                if enable is True:
                    dataw.append((date, open, close, high, low, vol))
                    open = close = high = low = vol = 0
                else:
                    enable = True
                date = item[0]
                open = item[1]
                high = item[3]
                low  = item[4]

            close = item[2]
            vol  += item[5]

            if high < item[3] : high = item[3]
            if low  > item[4] : low  = item[4]
               
        return  dataw
