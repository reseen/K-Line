from pack_graph   import *
from pack_target  import *
from pack_collect import *
from pack_storage import *


# 读取数据
def onGetData(code):
    db = storageStockA.storageStockA()
    # data = db.readData(code, '2016-01-01')
    data = db.readData(code)

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
    collect = collectStockA.collectStockA()
    collect.update(True, '000004.SZ')

    db = storageStockA.storageStockA()
    nm = target.norm()

    contents = db.readContents()
    normList = nm.getAllList()

    dataList = []
    for i in range(20):
        dataList.append((contents[i][0], contents[i][2]))

    gp = graph.graph(dataList, normList, onGetData, onGetNorm, onGetDataEx)
    gp.show()