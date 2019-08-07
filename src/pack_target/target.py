import numpy as np

MACD = 'MACD'
KDJ  = 'KDJ'
RSI  = 'RSI'
BOLL = 'BOLL'
ENE  = 'ENE'

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
    def __init__(self, xAxis = 0, xNum = 0, yAxis = 0, yNum = 0):
        self.xAxis = xAxis              # X轴坐标类型
        self.xNum = xNum                # X轴分割数量
        self.yAxis = yAxis              # Y轴坐标类型
        self.yNum = yNum                # Y轴分割数量

class param():
    def __init__(self, label = None, len = None, line = 0, color = None, axis = None):
        self.label = label
        self.line  = line
        self.color = color
        self.value = None if len is None else np.zeros(len)
        self.axis = axis

    def __str__(self):
        if self.label is None or self.data is None:
            return 'param is none'
        else:
            return 'param label = %s data length = %d' % (self.label, len(self.data))

class norm():
    def __init__(self):
        self.normList = (MACD, KDJ, RSI, BOLL, ENE)

    def getAllList(self):          # 获取当前库所支持的指标公式列表
        return self.normList

    def getMACD(self, data):
        dataLen = len(data)

        dataDIF = param('DIF', dataLen, LINE_LINE, COLOR_WHITE)
        dataDEA = param('DEA', dataLen, LINE_LINE, COLOR_PURPLE)
        dataBAR = param('BAR', dataLen, LINE_COLU, COLOR_AUTO, axis(AXIS_AUTO, 0, AXIS_CENTER, 0))  # 设该参数为主键

        EMA_12 = EMA_26 = DIF = DEA = BAR = 0
        ka = 2  / 13 
        kb = 11 / 13
        kc = 2  / 27 
        kd = 25 / 27
        ke = 2  / 10 
        kf = 8  / 10

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
