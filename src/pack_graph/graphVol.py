from OpenGL.GL import *

from . import graphPanel
import numpy as np

class graphVolume(graphPanel.graphPanel):

    def __init__(self, font, call = None):
        super().__init__(font, call)
        super().setMargin(graphPanel.gridMargin(10, 70))
        self.data = None
        self.primData = None
        self.dataMin = 0
        self.dataMax = 100

    # 设置成交量值
    def setData(self, data):
        self.primData = data
        self.dataLen = len(data)
        self.data = np.zeros([self.dataLen], np.int32)
        for i in range(self.dataLen):
            self.data[i] = data[i][5]

    # 设置选择索引
    def setIndex(self, begin, end, len):    
        super().setIndex(begin, end, len)

        if self.data is None : return
        self.dataMax = 0
        for i in range(begin, end + 1):
            if self.dataMax < self.data[i]:
                self.dataMax = self.data[i]

        self.dataMax = int(self.dataMax * 1.05)

    # 父类获取当前绘制的值颜色
    def onGetColor(self, index, id = 0):
        if self.primData is None : return (1.0, 1.0, 1.0, 0.5)
        if self.primData[index][2] > self.primData[index][1]:       # 收盘价大于开盘价
            return (1.0, 0.0, 0.0, 1.0)
        elif self.primData[index][2] < self.primData[index][1]:     # 收盘价大于开盘价
            return (0.0, 1.0, 0.0, 1.0)
        else:                                                       # 开盘价等于收盘价
            return (0.0, 0.5, 1.0, 1.0)

    # 父类获取当前选中的值 
    def onGetValue(self, index, id = 0):
        if self.data is None : return 0
        if index < 0 or index >= self.dataLen : return 0
        return self.data[index]

    # 绘图
    def draw(self):
        super().setRanges(self.dataMin, self.dataMax)
        super().drawInit()
        super().drawMargin()
        
        if self.data is None : return 
        super().drawCurveCloumn(self.data)
        super().drawChoice()
