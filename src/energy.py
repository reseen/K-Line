from pack_graph   import *
from pack_target  import *
from pack_collect import *
from pack_storage import *
import config as conf

# 读取数据
def onGetData(code):
    db = storageEnergy.storageEnergy(conf.PATH_DB_ENERGY)
    data = db.readData(code, '2015-01-01')
    # data = db.readData(code)

    for i in range(len(data)):              # 数据检查
        if data[i][1] == 0 and i != 0:
            lst = list(data[i])
            lst[1] = data[i - 1][2]         # 如果开盘价丢失，则用昨天收盘价代替
            tup = tuple(lst)
            data[i] = tup
    print("read %s success, data length = %d" % (code, len(data)))
    # return db.toWeek(data)
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
    config = conf.config()
    collect = collectEnergy.collectEnergy(config.public(), config.private(), conf.PATH_DB_ENERGY)
    collect.update()
    # collect.updateCSV('NG', '美国天然气连续', 'D:/期货日线数据1990-2019/天然气期货历史数据_1.csv')
    # collect.updateCSV('NG', '美国天然气连续', 'D:/期货日线数据1990-2019/天然气期货历史数据_2.csv')
    # collect.updateCSV('SC0', '纽约原油连续', 'D:/期货日线数据1990-2019/WTI原油期货历史数据_1.csv')
    # collect.updateCSV('SC0', '纽约原油连续', 'D:/期货日线数据1990-2019/WTI原油期货历史数据_2.csv')
    
    db = storageEnergy.storageEnergy(conf.PATH_DB_ENERGY)
    nm = target.norm()

    dataList = db.readList()
    normList = nm.getAllList()

    gp = graph.graph(dataList, normList, onGetData, onGetNorm, onGetDataEx)
    gp.show()