from OpenGL.GL import *

from . import graphPanel

class graphParam(graphPanel.graphPanel):
    def __init__(self, font, call = None):
        super().__init__(font, call)
        super().setMargin(graphPanel.gridMargin(10, 70))

    def setData(self, data):
        self.data = data            # 设置绘图数据

    def draw(self):
        super().setRanges(0, 30)
        super().drawInit()
        super().drawMargin()