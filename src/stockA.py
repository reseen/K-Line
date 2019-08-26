from pack_graph   import *
from pack_target  import *
from pack_collect import *
from pack_storage import *
import config as conf

# 读取数据
def onGetData(code):
    db = storageStockA.storageStockA(conf.PATH_DB_STOCKA)
    # data = db.readData(code, '2016-01-01')
    data = db.readData(code)
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
    if label == target.MACD: return nm.getMACD(data)
    if label == target.KDJ: return nm.getKDJ(data)
    if label == target.RSI: return nm.getRSI(data)
    return None

if __name__ == "__main__":

    config = conf.config()
    collect = collectStockA.collectStockA(config.public(), config.private(), conf.PATH_DB_STOCKA)

    db = storageStockA.storageStockA(conf.PATH_DB_STOCKA)
    nm = target.norm()
    
    updateList = []
    for item in collect.public['stockA']['list']:
        updateList.append(db.readContents(item)[0])

    # if collect.public['stockA']['all'] is True:
    #     collect.update()
    # else:
    #     collect.update(updateList)

    dataList = []
    normList = nm.getAllList()

    for item in updateList:
        dataList.append((item[0], item[2]))

    gp = graph.graph(dataList, normList, onGetData, onGetNorm, onGetDataEx)
    gp.show()