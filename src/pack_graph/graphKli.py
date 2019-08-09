from OpenGL.GL import *

from . import graphPanel
import numpy as np

class graphKline(graphPanel.graphPanel):

    def __init__(self, font, call = None):
        super().__init__(font, call, True)
        super().setMargin(graphPanel.gridMargin(10, 70, 10, 25, 100, 50))
        super().setFormat('%.02f')
        self.data = None
        self.dataLen = 0
        self.primData = None
        self.dataMin = 0
        self.dataMax = 100
        self.dataFmt = '%.02f'
        self.textBegin = None
        self.textBeginTid = None
        self.textEnd = None
        self.textEndTid = None
        self.textColor   = (255, 255, 255, 120)     # 文本颜色

    # 设置成交量值
    def setData(self, data):
        self.primData = data
        self.dataLen = len(data)
        self.data = np.zeros([self.dataLen, 4], np.float32)
        for i in range(self.dataLen):
            self.data[i][0] = data[i][1]
            self.data[i][1] = data[i][2]
            self.data[i][2] = data[i][3]
            self.data[i][3] = data[i][4]

    # 设置选择索引
    def setIndex(self, begin, end, len):    
        super().setIndex(begin, end, len)
        if self.primData is None : return
        if begin >= 0 and begin < self.dataLen:
            self.textBegin = self.font.number(self.primData[begin][0], self.textColor)
            self.textBeginTid = self.font.getTexture(self.textBegin)
        else:
            self.textBegin = None

        if end >= 0 and end < self.dataLen and end - begin == len - 1:
            self.textEnd = self.font.number(self.primData[end][0], self.textColor)
            self.textEndTid = self.font.getTexture(self.textEnd)
        else:
            self.textEnd = None

        self.dataMax = 0.0
        self.dataMin = 10000000.0
        for i in range(begin, end):
            if self.dataMax <= self.primData[i][1] : self.dataMax = self.primData[i][1]
            if self.dataMax <= self.primData[i][2] : self.dataMax = self.primData[i][2]
            if self.dataMax <= self.primData[i][3] : self.dataMax = self.primData[i][3]
            if self.dataMin >= self.primData[i][1] : self.dataMin = self.primData[i][1]                   
            if self.dataMin >= self.primData[i][2] : self.dataMin = self.primData[i][2]
            if self.dataMin >= self.primData[i][4] : self.dataMin = self.primData[i][4]

        dataRsv = (self.dataMax - self.dataMin) * 0.05    # 图像上下各预留5%
        self.dataMax = self.dataMax + dataRsv
        self.dataMin = self.dataMin - dataRsv

    # 获取数据颜色
    def getAutoColor(self, a, b):
        if a > b : return (1.0, 0.0, 0.0, 1.0)     # 红色
        if a < b : return (0.0, 1.0, 0.0, 1.0)     # 绿色
        else : return (0.0, 0.5, 1.0, 1.0)         # 蓝色

    # 父类获取当前绘制的值颜色
    def onGetColor(self, index, id = 0):
        if self.data is None : return (1.0, 1.0, 1.0, 0.5)
        return self.getAutoColor(self.data[index][1], self.data[index][0])

    # 父类获取当前绘制的数组颜色
    def onGetListColor(self, index, id = 0, sel = 0):
        if self.data is None : return (1.0, 1.0, 1.0, 0.5)

        if index == 0 : return self.getAutoColor(self.data[index][1], self.data[index][0])
        if sel == 0: return self.getAutoColor(self.data[index][0], self.data[index - 1][1])
        if sel == 1: return self.getAutoColor(self.data[index][2], self.data[index - 1][1])
        if sel == 2: return self.getAutoColor(self.data[index][3], self.data[index - 1][1])
        if sel == 3: return self.getAutoColor(self.data[index][1], self.data[index - 1][1])
        if sel == 4: return self.getAutoColor(self.data[index][1], self.data[index - 1][1])

        return (1.0, 1.0, 1.0, 0.5)

    # 父类获取当前选中的值 
    def onGetValue(self, index, id = 0):
        if self.primData is None : return 0
        if index < 0 or index >= self.dataLen : return 0
        return self.data[index][1]

    # 父类获取当前选中的列表
    def onGetList(self, index):
        if self.primData is None : return (0, 0, 0, 0, 0)
        if index < 0 or index >= self.dataLen : return (0, 0, 0, 0, 0)
        if index == 0:
            perc = (self.data[index][1] - self.data[index][0]) / self.data[index][0] * 100.00
        else:
            perc = (self.data[index][1] - self.data[index - 1][1]) / self.data[index - 1][1] * 100.00
        return (self.data[index][0], self.data[index][2], self.data[index][3], self.data[index][1], perc)

    # 父类获取当前选中的时间
    def onGetScale(self, index):
        if self.primData is None : return super().onGetScale(index)
        if index < 0 or index >= self.dataLen :return super().onGetScale(index)
        return self.primData[index][0]

    # 绘图
    def draw(self):
        super().setRanges(self.dataMin, self.dataMax)
        super().drawInit()
        super().drawMargin()
        if self.data is None : return 
        super().drawCurveCandle(self.data)
        super().drawChoice()
        super().drawScale(self.textBegin, self.textBeginTid, self.textEnd, self.textEndTid)
