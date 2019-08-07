
from OpenGL.GL import *

from pack_graph import graphSize

class graphLabel():
    def __init__(self, id, key, font, color):
        self.id = id
        self.font = font
        self.color = color

        self.font.setSpace(1)
        self.key = font.string('%s：' % key, color)
        self.keyTid = font.getTexture(self.key)
        self.value = None

    def setSize(self, x, y, width, height, frect):
        self.frect = frect
        self.rect = graphSize.rectEx(x, y, width, height, frect)

    def setValue(self, value, fmt):
        self.value = self.font.number(fmt % value, self.color)

    def draw(self):
        abs_x = self.frect.x + self.rect.x                                          # 计算绝对坐标值 X
        abs_y = self.frect.h + self.frect.y - self.rect.y - self.rect.h             # 计算绝对坐标值 Y  

        self.absrect = graphSize.rect(int(abs_x), int(abs_y), int(self.rect.w), int(self.rect.h))
        glViewport(self.absrect.x, self.absrect.y, self.absrect.w, self.absrect.h)  # 转换坐标 按钮内部坐标

        glColor4fv(self.color)                                                      # 设置按钮背景色

        font_w = self.key.shape[1]                      # 文本宽度
        font_h = self.key.shape[0]                      # 文本高度

        font_pw = font_w / self.rect.w
        font_ph = font_h / self.rect.h

        font_px = 0.0
        font_py = self.font.prec((1 - font_ph) / 2)     # 文本绘制纵轴坐标  
        
        self.font.drawTexture(self.keyTid, font_px, font_py, font_w, font_h, self.rect)

        if self.value is not None:
            font_w = self.value.shape[1]                # 文本宽度
            font_h = self.value.shape[0]                # 文本高度
            font_pw = font_w / self.rect.w
            font_ph = font_h / self.rect.h
            font_px = 1.0 - font_pw
            self.font.draw(self.value, font_px, font_py, font_w, font_h)
        glViewport(self.frect.x, self.frect.y, self.frect.w, self.frect.h)          # 还原坐标系