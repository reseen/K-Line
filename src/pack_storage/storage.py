import sqlite3

class database:
    def __init__(self, path = 'D:/K-Line/data/transaction.db'):
        self.path = path

    # 连接数据库
    def connect(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    # 数据库断开连接
    def disconnect(self):
        self.cursor.close()
        self.conn.close()

    # 判断表是否存在
    def __exist_table(self, name):
        self.cursor.execute('select count(*) from sqlite_master where type=\'table\' and name=\'%s\'' % name)
        count = self.cursor.fetchone()[0]
        return (True if(count != 0) else False)

    # 创建数据表 目录名称
    def __create_contents(self):
        self.cursor.execute('create table contents (code varchar(20) primary key, name text, modify datetime)')
    
    # 在目录内添加一个股票
    def __insert_contents(self, code, name, force):
        forcestr = ('replace' if force == True else 'ignore')
        SQL = 'insert or %s into contents (code, name, modify) values (\'%s\', \'%s\', datetime(\'now\', \'localtime\'))' % (forcestr, code, name)
        # print('SQL -> ', SQL)
        self.cursor.execute(SQL)
        self.conn.commit()

    # 读取目录
    def __read_contens(self):
        self.cursor.execute('select * from contents')
        return self.cursor.fetchall()

    # 删除一条目录
    def __delete_contents(self, code):
        SQL = 'delete from contents where code = \'%s\'' % code
        self.cursor.execute(SQL)
        self.conn.commit()

    # 创建数据表 股票代码
    def __create_datatable(self, code):
        self.cursor.execute('create table %s (date date primary key, open double, close double, high double, low double, vol double, modify datetime, remarks text)' % code)

    # 数据表内插入交易数据
    def __insert_datatable(self, code, date, open, close, high, low, vol, remarks, force):
        forcestr = ('replace' if force == True else 'ignore')
        SQL = 'insert or %s into %s (date, open, close, high, low, vol, modify, remarks) values (date(\'%s\'), %s, %s, %s, %s, %s, datetime(\'now\', \'localtime\'), \'%s\')' % \
            (forcestr, code, date, open, close, high, low, vol, 'null')
        # print('SQL -> ', SQL)
        self.cursor.execute(SQL)
        self.conn.commit()

    # 读取数据表
    def __read_datatable(self, code, start):
        SQL = None
        if start == None:
            SQL = 'select * from %s' % code
        else:
            SQL = 'select * from %s where date >= date(\'%s\')' % (code, start) 
        # print('SQL -> ', SQL)
        self.cursor.execute(SQL)
        return self.cursor.fetchall()

    # 删除数据表
    def __delete_datatable(self, code):
        self.cursor.execute('drop table %s' % code)

    #-------------------------------------------------------------------------------------------#

    # 创建数据表
    def create_data(self, code, name, force = False):
        if self.__exist_table('contents') == False:     # 创建目录
            self.__create_contents()

        if self.__exist_table(code) == False:
            self.__create_datatable(code)               # 创建表
        
        self.__insert_contents(code, name, force)       # 添加目录

    # 插入数据
    def insert_data(self, code, date, open, close, high, low, vol, remarks = 'null', force = False):
        self.__insert_datatable(code, date, open, close, high, low, vol, remarks, force)

    # 读取数据库列表
    def read_datalist(self):
        return self.__read_contens()

    # 读取数据
    def read_data(self, code, start = None):
        return self.__read_datatable(code, start)

    # 删除数据表 股票代码
    def delete_data(self, code):
        self.__delete_contents(code)                # 删除目录
        self.__delete_datatable(code)               # 删除表

if __name__ == "__main__":

    db = database()
    db.connect()

    list = db.read_datalist()
    print(list)

    datas = db.read_data('NG', '2019-01-01')
    for data in datas:
        print(data)