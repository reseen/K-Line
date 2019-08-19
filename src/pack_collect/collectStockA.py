
from pack_storage.storageStockA import storageStockA as stStockA
import tushare as ts 
import datetime
import time


pro = ts.pro_api('4e5e2d7fbf14185d371c9a5e78d178882d2b91436a0de40599a29ece')



class collectStockA():
    def __init__(self, path = 'D:/K-Line/data/list.json'):
        self.path = path

    # 获取当前日期
    def __getDateNow(self, fmt = '%Y_%m_%d'):
        return datetime.datetime.now().strftime(fmt)

    # 更新数据
    def update(self, force = False):
        self.updateContents(force)

    # 更新目录
    def updateContents(self, force = False):
        db = stStockA()

        ts.set_token('4e5e2d7fbf14185d371c9a5e78d178882d2b91436a0de40599a29ece')

        # 获取所有股票名称
        # data = pro.stock_basic(exchange = '', list_status = '', fields = 'ts_code, symbol, name, area, industry, fullname, enname, market, exchange, curr_type, list_status, list_date, delist_date')
        # db.updateContents(data, force)

        list = db.readContents()
        for i in range(len(list)):
            data = ts.pro_bar(ts_code = list[i][0], adj = 'qfq', start_date = '20000101', end_date = self.__getDateNow('%Y%m%d'))
            db.update(list[i][0], data, force)
            print("update success %s %s" % (list[i][0], list[i][2]))
            time.sleep(0.3)



