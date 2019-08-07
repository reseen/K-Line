from OpenGL.GL import *

from . import graphPanel
import numpy as np

class graphParam(graphPanel.graphPanel):
    def __init__(self, font, call = None):
        super().__init__(font, call)
        super().setMargin(graphPanel.gridMargin(10, 70))
        super().setFormat('%.02f')

        self.data = None
        self.dataNum = 0
        self.dataLen = 0
        self.dataMin = 0.0
        self.dataMax = 100.0

    def setData(self, data):
        self.data = data                    # 设置绘图数据
        self.dataNum = len(self.data)
        self.dataLen = len(self.data[0].value)
    
    # 设置选择索引
    def setIndex(self, begin, end, len):    
        super().setIndex(begin, end, len)
        if self.data is None : return

        self.dataMin = 10000.0
        self.dataMax = -10000.0
        for item in self.data:
            for i in range(begin, end + 1):
                if self.dataMax < item.value[i] : self.dataMax = item.value[i]
                if self.dataMin > item.value[i] : self.dataMin = item.value[i]

        dataRsv = (self.dataMax - self.dataMin) * 0.05    # 图像上下各预留5%
        self.dataMax = self.dataMax + dataRsv
        self.dataMin = self.dataMin - dataRsv

        print(self.dataMax, self.dataMin)

    # 父类获取当前绘制的值颜色
    def onGetColor(self, index, id = 0):
        if self.data is None : return (1.0, 1.0, 1.0, 0.5)

        if self.data[2].value[index] > 0.0:            # 值大于0
            return (1.0, 0.0, 0.0, 1.0)
        elif self.data[2].value[index] < 0.0:          # 值小于0
            return (0.0, 1.0, 0.0, 1.0)
        else:                                               # 值等于0
            return (0.0, 0.5, 1.0, 1.0)

    # 父类获取当前选中的值 
    # def onGetValue(self, index):
    #     if self.primData is None : return 0
    #     if index < 0 or index >= self.dataLen : return 0
    #     return self.data[index][1]

    # 父类获取当前选中值的标记
    def onGetScale(self, index):
        if self.primData is None : return super().onGetScale(index)
        if index < 0 or index >= self.dataLen :return super().onGetScale(index)
        return self.primData[index][0]

    def draw(self):
        super().setRanges(self.dataMin, self.dataMax)
        super().drawInit()
        super().drawMargin()
        if self.data is None : return 
        super().drawCurveCloumn(self.data[2].value)