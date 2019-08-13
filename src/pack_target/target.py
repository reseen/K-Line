import numpy as np

MACD = 'MACD'
KDJ  = 'KDJ'
RSI  = 'RSI'

LINE_LINE   =   0       # 折线图
LINE_COLU   =   1       # 柱形图

COLOR_AUTO   = None                     # 自动着色
COLOR_WHITE  = (1.0, 1.0, 1.0, 1.0)     # 白色
COLOR_RED    = (1.0, 0.0, 0.0, 1.0)     # 红色
COLOR_GREEN  = (0.0, 1.0, 0.0, 1.0)     # 绿色
COLOR_BLUE   = (0.0, 0.5, 1.0, 1.0)     # 蓝色
COLOR_PURPLE = (1.0, 0.0, 1.0, 1.0)     # 紫色
COLOR_ORANGE = (1.0, 0.5, 0.0, 1.0)     # 橙色

AXIS_AUTO    = 0                        # 自动坐标
AXIS_FIXED   = 1                        # 固定坐标
AXIS_CENTER  = 2                        # 居中坐标 

class axis():
    def __init__(self, type = 0, num = 0, fmt = '%.02f'):
        self.type = type                # 轴坐标类型 仅针对Y轴
        self.num = num                  # 轴分割数量
        self.fmt = fmt                  # 坐标轴格式


class param():
    def __init__(self, label = None, len = None, line = 0, color = None, fmt = '%.02f', axis = None):
        self.label = label
        self.line  = line
        self.color = color
        self.value = None if len is None else np.zeros(len)
        self.axis = axis
        self.fmt = fmt

    def __str__(self):
        if self.label is None or self.value is None:
            return 'param is none'
        else:
            return 'param label = %s data length = %d' % (self.label, len(self.value))

class norm():
    def __init__(self):
        self.normList = (MACD, KDJ, RSI)

    def getAllList(self):          # 获取当前库所支持的指标公式列表
        return self.normList

    # 计算MA值
    def getMA(self, data, cycle = 5, color = COLOR_WHITE):
        dataLen = len(data)
        dataMA = param('MA%d' % cycle, dataLen, LINE_LINE, color)

        for i in range(dataLen):
            st = i - cycle
            if st < 0:
                dataMA.value[i] = 0
            else:
                sum = 0
                for j in range(st, i) : sum += data[j][2]
                dataMA.value[i] = sum / (i - st)
        return dataMA

    # 计算成交量MA值
    def getMAVOL(self, data, cycle = 5, color = COLOR_WHITE):
        dataLen = len(data)
        dataMAVOL = param('MV%d' % cycle, dataLen, LINE_LINE, color, '%d')

        for i in range(dataLen):
            st = i - cycle
            if st < 0:
                dataMAVOL.value[i] = 0
            else:
                sum = 0
                for j in range(st, i) : sum += data[j][5]
                dataMAVOL.value[i] = int(sum / (i - st))
        return dataMAVOL

    # 计算K线MACD
    def getMACD(self, data):
        dataLen = len(data)
        dataDIF = param('DIF', dataLen, LINE_LINE, COLOR_BLUE)
        dataDEA = param('DEA', dataLen, LINE_LINE, COLOR_PURPLE)
        dataBAR = param('BAR', dataLen, LINE_COLU, COLOR_AUTO, '%.02f', axis(AXIS_CENTER, 1))  # 设该参数为主键

        EMA_12 = EMA_26 = DIF = DEA = BAR = 0
        ka, kb = 2 / 13, 11 / 13
        kc, kd = 2 / 27, 25 / 27
        ke, kf = 2 / 10,  8 / 10

        for i in range(dataLen):
            if i != 0:
                EMA_12 = data[i][2] * ka + EMA_12 * kb
                EMA_26 = data[i][2] * kc + EMA_26 * kd
                DIF = EMA_12 - EMA_26
                DEA = DIF * ke + DEA * kf
                BAR = (DIF - DEA) * 2

            dataDIF.value[i] = DIF
            dataDEA.value[i] = DEA
            dataBAR.value[i] = BAR
        
        return (dataDIF, dataDEA, dataBAR)


    def __RSV(self, index, data, n):
        Cn = data[index][2]
        Ln = data[index][4]
        Hn = data[index][4]

        start = index - n - 1
        if index < 0 : index = 0
        for i in (start, index):
            if Hn < data[i][3] : Hn = data[i][3]
            if Ln > data[i][4] : Ln = data[i][4]

        if Hn == Ln : return 0
        return (Cn - Ln) / (Hn - Ln) * 100
    
    # 计算K线KDJ
    def getKDJ(self, data):
        dataLen = len(data)
        dataK = param('K', dataLen, LINE_LINE, COLOR_BLUE)
        dataD = param('D', dataLen, LINE_LINE, COLOR_PURPLE)
        dataJ = param('J', dataLen, LINE_LINE, COLOR_ORANGE, '%.02f', axis(AXIS_AUTO, 0))  # 设该参数为主键

        lastK = 50
        lastD = 50
        for i in range(dataLen):
            K = 2 / 3 * lastK + 1 / 3 * self.__RSV(i, data, 9)
            D = 2 / 3 * lastD + 1 / 3 * K
            J = 3 * K - 2 * D
            dataK.value[i] = K
            dataD.value[i] = D
            dataJ.value[i] = J
            lastK = K
            lastD = D

        return (dataK, dataD, dataJ)

    def __RSI(self, index, data, n):
        if index <= n : return 0
        A = B = D = 0
        for i in range(index - n, index):
            D = data[i][2] - data[i - 1][2]
            if D > 0 : A += D
            if D < 0 : B += abs(D)
        return A / (A + B) * 100

    #计算RSI  
    def getRSI(self, data):
        dataLen = len(data)
        dataR6  = param('R6', dataLen, LINE_LINE, COLOR_BLUE, '%.02f', axis(AXIS_AUTO, 0))  # 设该参数为主键
        dataR12 = param('R12', dataLen, LINE_LINE, COLOR_PURPLE)
        dataR24 = param('R24', dataLen, LINE_LINE, COLOR_ORANGE) 

        for i in range(dataLen):
            dataR6.value[i]  = self.__RSI(i, data, 6)
            dataR12.value[i] = self.__RSI(i, data, 12)
            dataR24.value[i] = self.__RSI(i, data, 24)
        return (dataR6, dataR12, dataR24)