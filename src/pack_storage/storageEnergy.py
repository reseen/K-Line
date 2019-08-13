from . import storageBase

class storageEnergy(storageBase.database):

    def __init__(self, path = 'D:/K-Line/data/energy.db'):
        super().__init__(path)

    # 目录管理-------------------------------------------------------------
    
    # 创建目录
    def __create_contents(self):                        
        super().execute('create table contents (code varchar(20) primary key, name text, modify datetime)')

    # 添加/修改目录
    def __insert_contents(self, code, name, force):     
        forcestr = 'replace' if force == True else 'ignore'
        SQL = 'insert or %s into contents (code, name, modify) values (\'%s\', \'%s\', datetime(\'now\', \'localtime\'))' % (forcestr, code, name)
        # print('SQL -> ', SQL)
        super().execute(SQL)
        super().commit()

    # 删除目录
    def __delete_contents(self, code):                  
        SQL = 'delete from contents where code = \'%s\'' % code
        super().execute(SQL)
        super().commit()

    # 读取目录
    def __read_contens(self):                           
        super().execute('select * from contents')
        return super().fetchall()

    # 数据管理-------------------------------------------------------------

    # 创建数据表 股票代码
    def __create_datatable(self, code):                
        super().execute('create table %s (date date primary key, open double, close double, high double, low double, vol double, modify datetime, remarks text)' % code)
    
    # 删除数据表
    def __delete_datatable(self, code):                 
        super().execute('drop table %s' % code)

    # 添加/修改数据表
    def __insert_datatable(self, code, date, open, close, high, low, vol, remarks, force):
        forcestr = 'replace' if force == True else 'ignore'
        SQL = 'insert or %s into %s (date, open, close, high, low, vol, modify, remarks) values (date(\'%s\'), %s, %s, %s, %s, %s, datetime(\'now\', \'localtime\'), \'%s\')' % (forcestr, code, date, open, close, high, low, vol, 'null')
        # print('SQL -> ', SQL)
        super().execute(SQL)
        super().commit()

    # 读取数据表
    def __read_datatable(self, code, start):
        if start == None:
            SQL = 'select * from %s' % code
        else:
            SQL = 'select * from %s where date >= date(\'%s\')' % (code, start) 
        # print('SQL -> ', SQL)
        super().execute(SQL)
        return super().fetchall()

    # public 能源数据库管理接口----------------------------------------------

    # 创建数据表
    def create(self, code, name, force = False):
        if super().existTable('contents') == False:     # 创建目录
            self.__create_contents()

        if super().existTable(code) == False:           # 创建表
            self.__create_datatable(code)               
        
        self.__insert_contents(code, name, force)       # 添加目录

    # 删除数据表 股票代码
    def delete(self, code):
        self.__delete_contents(code)                    # 删除目录
        self.__delete_datatable(code)                   # 删除表
    
    # 插入数据
    def insertData(self, code, date, open, close, high, low, vol, remarks = 'null', force = False):
        self.__insert_datatable(code, date, open, close, high, low, vol, remarks, force)
    
    # 读取数据库列表
    def readList(self):
        return self.__read_contens()
    
    # 读取数据
    def readData(self, code, start = None):
        return self.__read_datatable(code, start)
    