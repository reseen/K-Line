from pack_storage import *
from pack_graph   import *
from pack_target  import *

import requests
import datetime
import json


# 获取配置文件
def getConfig(path = '../data/list.json'):
    try:
        with open(path, 'r', encoding = 'UTF-8') as f:    # 打开文件
            sconfig = f.read()                            # 读取文件
            return json.loads(sconfig)
    except:
        print('配置文件"list.json"不存在，请检查。')

# 获取当前日期
def getDateNow(fmt = '%Y_%m_%d'):
    return datetime.datetime.now().strftime(fmt)

# 获取数据路径
def getDataURL(date, url):
    return url.replace('{YYYY_MM_DD}', date)

# 获取数据
def getData(url):
    response = requests.get(url)
    lts = response.text.find('(')
    rts = response.text.find(')')
    dat = response.text[lts + 1: rts]
    return json.loads(dat)

# 更新数据
def updateData(force = False):
    config = getConfig()
    for energy in config['energy']:
        dateURL = getDataURL(date = getDateNow(), url = energy['url'])
        datas = getData(dateURL)
        db = storage.database()
        db.connect()
        db.create_data(energy['code'], energy['name'], force)
        for data in datas:
            if 'date' in data:
                db.insert_data(energy['code'], data['date'], data['open'], data['close'], data['high'], data['low'], data['volume'], 'null', force)
            elif 'd' in data:
                db.insert_data(energy['code'], data['d'], data['o'], data['c'], data['h'], data['l'], data['v'], 'null', force)
            else:
                print('--->', data)
        print('update finish [%s - %s]' % (energy['code'], energy['name']))

def onGetData(code):
    db = storage.database()
    db.connect()
    data = db.read_data(code, '2018-01-01')
    # data = db.read_data(code)
    db.disconnect()
    return data

def onGetNorm(label, data):
    nm = target.norm()
    if label == target.MACD : return nm.getMACD(data)
    
    return None

if __name__ == "__main__":
    # updateData()

    db = storage.database()

    db.connect()
    dataList = db.read_datalist()
    db.disconnect()

    # print(list)
    # datas = db.read_data('NG', '2019-01-01')

    nm = target.norm()
    normList = (target.MACD, target.KDJ, target.RSI)

    gp = graph.graph(dataList, nm.getAllList(), onGetData, onGetNorm)
    gp.show()

    # for data in datas:
    #     print(data)
    
    # db.create_data('NG', '美国天然气')
 
    # for data in datas:
    #     db.insert_data('NG', data)

    # db.delete_data('NG')
    # db.disconnect()
    print("OK")