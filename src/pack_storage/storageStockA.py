from . import storageBase

DEFAULT_STARTTIME   =   '20000101'      # 默认起始时间

class storageStockA(storageBase.database):

    def __init__(self, path = 'D:/K-Line/data/stockA.db'):
        super().__init__(path)

    # 目录管理-------------------------------------------------------------

    # 创建目录
    def __create_contents(self):                
        super().execute('create table contents (code varchar(20) primary key, symbol varchar(20), name text, area text, \
            industry text, fullname text, enname text, market text, exchange text, curr_type text, list_status text, list_date text, \
            delist_date text, is_hs text, modify datetime)')

    # 添加/修改目录
    def __insert_contents(self, data, force = False):     
        forcestr = 'replace' if force == True else 'ignore'
        for i in range(len(data.ts_code)):
            SQL = 'insert or %s into contents (code, symbol, name, area, industry, fullname, enname, market, exchange, curr_type, list_status, list_date, delist_date, modify) \
                values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', datetime(\'now\', \'localtime\'))' \
                % (forcestr, data.ts_code[i], data.symbol[i], data.name[i], data.area[i], data.industry[i], data.fullname[i], data.enname[i].replace('\'', '\'\''), data.market[i], data.exchange[i], data.curr_type[i], data.list_status[i], data.list_date[i], data.delist_date[i])
            
            # print('SQL -> ', SQL)
            super().execute(SQL)
            super().commit()
            # print("insert success [%d] %s %s" % (i, data.ts_code[i], data.name[i]))

    # 删除目录
    def __delete_contents(self, code):                  
        SQL = 'delete from contents where code = \'%s\'' % code
        super().execute(SQL)
        super().commit()
    
    # 清除目录
    def __drop_contents(self, code):                 
        super().execute('drop table contents')

    # 读取目录
    def __read_contens(self):                           
        super().execute('select * from contents')
        return super().fetchall()

    # 数据管理-------------------------------------------------------------
    def __fmt_code(self, code):
        list = code.split(".", 1)
        return "%s%s" % (list[1], list[0])

    def __fmt_date(self, date):
        return "%s-%s-%s" % (date[0:4], date[4:6], date[6:8])

    # 创建数据表 股票代码
    def __create_datatable(self, code):        
        code = self.__fmt_code(code)  
        super().execute('create table %s (date date primary key, open double, close double, high double, low double, vol double, modify datetime, remarks text)' % code)

    # 删除数据表
    def __delete_datatable(self, code):     
        code = self.__fmt_code(code)             
        super().execute('drop table %s' % code)

    # 添加/修改数据表
    def __insert_datatable(self, code, date, open, close, high, low, vol, remarks, force):
        forcestr = 'replace' if force == True else 'ignore'
        code = self.__fmt_code(code) 
        date = self.__fmt_date(date)
        SQL = 'insert or %s into %s (date, open, close, high, low, vol, modify, remarks) values (date(\'%s\'), %s, %s, %s, %s, %s, datetime(\'now\', \'localtime\'), \'%s\')' % (forcestr, code, date, open, close, high, low, vol, 'null')
        # print('SQL -> ', SQL)
        super().execute(SQL)
        super().commit()

    # 读取数据表
    def __read_datatable(self, code, start):
        code = self.__fmt_code(code) 
        if start == None:
            SQL = 'select * from %s order by date asc' % code
        else:
            SQL = 'select * from %s where date >= date(\'%s\') order by date asc' % (code, start) 
        # print('SQL -> ', SQL)
        super().execute(SQL)
        return super().fetchall()

    # 读取最后一天数据
    def __read_datalast(self, code):
        code = self.__fmt_code(code) 
        SQL = "select * from %s order by date desc limit 1" % code
        super().execute(SQL)
        return super().fetchall()

    # 更新数据表
    def updateContents(self, data, force = False):
        if super().existTable('contents') == False:     # 创建目录
            self.__create_contents()
        self.__insert_contents(data, force)

    # 最后一次更新时间
    def getLastTime(self, code):
        if super().existTable(self.__fmt_code(code)) == False:
            return DEFAULT_STARTTIME

        data = self.__read_datalast(code)
        if len(data) == 0:
            return DEFAULT_STARTTIME
            
        return data[0][0].replace('-', '')

    def getDefaultTime(self):
        return DEFAULT_STARTTIME

    # 更新数据表
    def update(self, code, data, force = False):
        if super().existTable(self.__fmt_code(code)) == False:   # 创建目录
            self.__create_datatable(code)

        for i in range(len(data.ts_code)):
            self.__insert_datatable(code, data.trade_date[i], data.open[i], data.close[i], data.high[i], data.low[i], data.vol[i], 'null', force)

    # 读取数据库目录
    def readContents(self):
        return self.__read_contens()

    # 读取数据
    def readData(self, code, start = None):
        return self.__read_datatable(code, start)