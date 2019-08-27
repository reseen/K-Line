# 获取能源期货数据

from pack_storage.storageEnergy import storageEnergy as stEnergy

import requests
import datetime
import json
import csv

class collectEnergy():
    def __init__(self, pubcfg, prvcfg, path):
        self.path = path
        self.public = pubcfg
        self.private = prvcfg

    # 获取当前日期
    def __getDateNow(self, fmt = '%Y_%m_%d'):
        return datetime.datetime.now().strftime(fmt)

    # 获取数据路径
    def __getDataURL(self, date, url):
        return url.replace('{YYYY_MM_DD}', date)

    # 获取数据
    def __getData(self, url):
        response = requests.get(url)
        lts = response.text.find('(')
        rts = response.text.find(')')
        dat = response.text[lts + 1: rts]
        return json.loads(dat)

    # 更新数据
    def update(self, force = False):
        for energy in self.public['energy']:
            dateURL = self.__getDataURL(date = self.__getDateNow(), url = energy['url'])
            datas = self.__getData(dateURL)
            db = stEnergy(self.path)
            db.create(energy['code'], energy['name'], force)
            for data in datas:
                if 'date' in data:
                    db.insertData(energy['code'], data['date'], data['open'], data['close'], data['high'], data['low'], data['volume'], 'null', force)
                elif 'd' in data:
                    db.insertData(energy['code'], data['d'], data['o'], data['c'], data['h'], data['l'], data['v'], 'from url', force)
                else:
                    print('--->', data)
            print('update finish [%s - %s] data len = %d' % (energy['code'], energy['name'], len(datas)))
    
    # 从CSV文件中更新数据
    def updateCSV(self, code, name, path, force = False):
        with open(path, encoding = 'utf-8') as f:
            csvf = csv.reader(f)
            head = True

            db = stEnergy(self.path)
            db.create(code, name, force)
            for row in csvf:
                if head is True: 
                    head = False
                else:
                    date = datetime.datetime.strptime(row[0], '%Y年%m月%d日').strftime('%Y-%m-%d')
                    if row[5] == '-':
                        vol = 0.0 
                    else:
                        vol = float(row[5][0:-1]) * 1000.00
                    db.insertData(code, date, row[2], row[1], row[3], row[4], vol, 'from csv', force)
        print("update CSV success %s" % path)

