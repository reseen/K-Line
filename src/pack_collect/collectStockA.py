
from pack_storage.storageStockA import storageStockA as stStockA
import tushare as ts 
import datetime
import time


class collectStockA():
    def __init__(self, pubcfg, prvcfg, path):
        self.path = path
        self.public = pubcfg
        self.private = prvcfg

    # 获取当前日期
    def __getDateNow(self, fmt = '%Y_%m_%d'):
        return datetime.datetime.now().strftime(fmt)

    # 更新数据
    def update(self, list = None, force = False, code = None):
        ts.set_token(self.private['tusharetoken'])
        pro = ts.pro_api()
        db = stStockA(self.path)

        if list is None:
            # 更新股票目录
            data = pro.stock_basic(exchange = '', list_status = '', fields = 'ts_code, symbol, name, area, industry, fullname, enname, market, exchange, curr_type, list_status, list_date, delist_date')
            db.updateContents(data, True)       # 强制更新 股票状态可能会变
            print("Contents update success")

        # 强制更新单条数据
        if code is not None:
            start = db.getDefaultTime()
            data = ts.pro_bar(ts_code = code, adj = 'qfq', start_date = start, end_date = self.__getDateNow('%Y%m%d'))
            db.update(code, data, force)
            print("Update success %s  -Time from %s to now  -Number = %-5d" % (code, start, len(data.trade_date)))
            return

        # 根据目录依次更新数据
        if list is None : list = db.readContents()
        for i in range(len(list)):
            start = db.getLastTime(list[i][0])
            data = ts.pro_bar(ts_code = list[i][0], adj = 'qfq', start_date = start, end_date = self.__getDateNow('%Y%m%d'))
            db.update(list[i][0], data, force)
            # Tushare限制 每分钟请求200次
            time.sleep(0.3) 
            print("% 4d/%d Update success %s  -Time from %s to now  -Number = %-5d  -Name = %s" % (i + 1, len(list), list[i][0], start, len(data.trade_date), list[i][2]))