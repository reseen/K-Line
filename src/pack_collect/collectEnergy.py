

from pack_storage.storageEnergy import storageEnergy as stEnergy

import requests
import datetime
import json

class collectEnergy():
    def __init__(self, path = 'D:/K-Line/data/list.json'):
        self.path = path

    # 获取配置文件
    def __getConfig(self, path):
        try:
            with open(path, 'r', encoding = 'UTF-8') as f:    # 打开文件
                sconfig = f.read()                            # 读取文件
                return json.loads(sconfig)
        except:
            print('配置文件"list.json"不存在，请检查。')

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
        config = self.__getConfig(self.path)
        for energy in config['energy']:
            dateURL = self.__getDataURL(date = self.__getDateNow(), url = energy['url'])
            datas = self.__getData(dateURL)
            db = stEnergy()
            db.create(energy['code'], energy['name'], force)
            for data in datas:
                if 'date' in data:
                    db.insertData(energy['code'], data['date'], data['open'], data['close'], data['high'], data['low'], data['volume'], 'null', force)
                elif 'd' in data:
                    db.insertData(energy['code'], data['d'], data['o'], data['c'], data['h'], data['l'], data['v'], 'null', force)
                else:
                    print('--->', data)
            print('update finish [%s - %s] data len = %d' % (energy['code'], energy['name'], len(datas)))