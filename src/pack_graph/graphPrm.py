from OpenGL.GL import *

from . import graphPanel
import numpy as np

LINE_LINE   = 0    # 折线图
LINE_COLU   = 1    # 柱形图

AXIS_AUTO   = 0    # 自动坐标
AXIS_FIXED  = 1    # 固定坐标
AXIS_SYMMET = 2    # 对称坐标 

class graphParam(graphPanel.graphPanel):
    def __init__(self, font, call = None):
        super().__init__(font, call)
        super().setMargin(graphPanel.gridMargin())
        
        self.data = None
        self.dataNum = 0
        self.dataLen = 0
        self.dataMin = 0.0
        self.dataMax = 100.0
        self.axis = None
        self.axisIndex = 0

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
        for index in range(self.dataNum):
            for i in range(begin, end + 1):
                if self.dataMax < self.data[index].value[i] : self.dataMax = self.data[index].value[i]
                if self.dataMin > self.data[index].value[i] : self.dataMin = self.data[index].value[i]
            if self.axis is None and self.data[index].axis is not None:
                self.axis = self.data[index].axis
                self.axisIndex = index
                if self.axis.type == AXIS_AUTO:
                    super().setMargin(graphPanel.gridMargin())
                if self.axis.type == AXIS_FIXED or self.axis.type == AXIS_SYMMET:
                    super().setMargin(graphPanel.gridMargin(height = self.axis.num, fixed = True))
                super().setFormat(self.axis.fmt)

        dataRsv = self.dataMax - self.dataMin * 0.05    # 图像上下各预留5%
        self.dataMax = self.dataMax + dataRsv
        self.dataMin = self.dataMin - dataRsv

        self.dataMax = int(self.dataMax * 10) / 10.00
        self.dataMin = int(self.dataMin * 10) / 10.00

        if self.axis is not None:
            if self.axis.type == AXIS_SYMMET:
                self.dataMax = abs(self.dataMax) if abs(self.dataMax) > abs(self.dataMin) else abs(self.dataMin)
                self.dataMin = 0 - self.dataMax

    # 父类获取当前绘制的值颜色
    def onGetColor(self, index, id = 0):
        if self.data is None:
            return (1.0, 1.0, 1.0, 0.5)

        if self.data[id].color is None:
            if self.data[id].value[index] > 0.0:        # 值大于0
                return (1.0, 0.0, 0.0, 1.0)
            elif self.data[id].value[index] < 0.0:      # 值小于0
                return (0.0, 1.0, 0.0, 1.0)
            else:                                       # 值等于0
                return (0.0, 0.5, 1.0, 1.0)
        else:
            return self.data[id].color

    # 父类获取当前选中的值 
    def onGetValue(self, index, id = 0):
        if self.data is None : return 0
        if index < 0 or index >= self.dataLen : return 0
        return self.data[2].value[index]

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
        super().drawCurveLine(self.data[0].value, 0)
        super().drawCurveLine(self.data[1].value, 1)
        super().drawCurveCloumn(self.data[2].value, 2)
        super().drawChoice()