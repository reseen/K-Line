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

# 读取数据
def onGetData(code):
    db = storage.database()
    db.connect()
    # data = db.read_data(code, '2018-01-01')
    data = db.read_data(code)
    db.disconnect()

    for i in range(len(data)):              # 数据检查
        if data[i][1] == 0 and i != 0:
            lst = list(data[i])
            lst[1] = data[i - 1][2]         # 如果开盘价丢失，则用昨天收盘价代替
            tup = tuple(lst)
            data[i] = tup
    print("read %s success, data length = %d" % (code, len(data)))
    return data

# K线叠加图像
def onGetDataEx(index, data):
    if data is None : return None
    nm = target.norm()
    if index == 0:
        MA5 = nm.getMA(data, 5, target.COLOR_BLUE)
        MA30 = nm.getMA(data, 30, target.COLOR_PURPLE)
        MA250 = nm.getMA(data, 250, target.COLOR_ORANGE)
        return (MA5, MA30, MA250)
    if index == 1:
        MAVOL5 = nm.getMAVOL(data, 5, target.COLOR_BLUE)
        MAVOL10 = nm.getMAVOL(data, 15, target.COLOR_PURPLE)
        return (MAVOL5, MAVOL10)
    
# 参数图像
def onGetNorm(label, data):
    if data is None : return None
    nm = target.norm()
    if label == target.MACD : return nm.getMACD(data)
    if label == target.KDJ: return nm.getKDJ(data)
    if label == target.RSI: return nm.getRSI(data)
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
    normList = nm.getAllList()

    gp = graph.graph(dataList, normList, onGetData, onGetNorm, onGetDataEx)
    gp.show()

    # for data in datas:
    #     print(data)
    
    # db.create_data('NG', '美国天然气')
 
    # for data in datas:
    #     db.insert_data('NG', data)

    # db.delete_data('NG')
    # db.disconnect()
    print("OK")