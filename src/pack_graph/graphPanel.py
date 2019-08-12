from OpenGL.GL import *

from . import graphSize
from . import winConfig

from abc import ABCMeta, abstractmethod

import datetime as dt

LINE_LINE   = 0    # 折线图
LINE_COLU   = 1    # 柱形图

# 定义网格尺寸类
class gridMargin():
    def __init__(self, left = 10, right = 70, top = 10, bottom = 10, width = 100, height = 40, fixed = False):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.gridWidth = width          # 网格宽度 px
        self.gridHeight = height        # 网格高度 px
        self.fixed = fixed              # 网格是否固定  仅Y轴有效

# 定义选择索引类
class index():
    def __init__(self, begin = 0, end = 50, length = 50):
        self.begin = begin              # 绘图起始索引
        self.end = end                  # 绘图结束索引
        self.length = length            # 绘图长度长度

# 绘图板基类
class graphPanel():
    __metaclass__ = ABCMeta

    def __init__(self, font, call = None, label = False):
        self.margin = gridMargin()      # 定义网格
        self.index = index()        # 定义索引
        self.call = call            # 选择回调
        self.font = font            # 显示字体
        self.size = None            # 面板尺寸
        self.valMin = 0             # 最小值
        self.valMax = 100           # 最大值
        self.format = '%d'          # 坐标显示格式

        self.clicked = 0            # 是否被点击
        self.choice = -1            # 当前选中的值
        self.choiceLast = -1        # 前一次选中的K线

        self._left   = 0
        self._right  = 0
        self._top    = 0
        self._bottom = 0
        self._num    = 0
        self._uint   = 0
        self._uintPx = 0

        self.moveState = False      # 移动状态
        self.movePointX = 0         # 移动坐标
        self.movePointY = 0         # 移动坐标
        
        self.colorMargin = (1.0, 1.0, 1.0, 0.2)     # 边框颜色
        self.colorGrid   = (1.0, 1.0, 1.0, 0.1)     # 网格颜色
        self.colorText   = (255, 255, 255, 120)     # 文本颜色
        self.colorWhite  = (255, 255, 255, 220)     # 文本亮色

        self.fontLabel = []
        self.fontLabelTid = []
        if label is True:
            self.font.setSpace(0)
            self.fontLabel.append(self.font.string('OPEN：', self.colorText))
            self.fontLabel.append(self.font.string('HIGH：', self.colorText))
            self.fontLabel.append(self.font.string('LOW：', self.colorText))
            self.fontLabel.append(self.font.string('CLOSE：', self.colorText))
            self.fontLabel.append(self.font.string('PERC：', self.colorText))
            for img in self.fontLabel:
                self.fontLabelTid.append(self.font.getTexture(img))

    def setMargin(self, margin):                    # 设置面板边距
        self.margin = margin

    def setSize(self, frect):                       # 设置面板尺寸
        self.size = frect           
        self.row = int((self.size.w - self.margin.left - self.margin.right) / self.margin.gridWidth)
        if self.margin.fixed == True:
            self.col = self.margin.gridHeight + 1
        else:
            self.col = int((self.size.h - self.margin.top - self.margin.bottom) / self.margin.gridHeight)

    def setFormat(self, format):
        self.format = format

    def setRanges(self, min, max):                  # 设置取值范围
        self.valMin = min
        self.valMax = max

    def setIndex(self, begin, end, len):            # 设置选择范围
        self.index.begin = begin
        self.index.end = end
        self.index.length = len

    def setChoice(self, choice):
        self.choice = choice

    def setMarginColor(self, color):        # 设置边框颜色
        self.colorMargin = color

    def setGridColor(self, color):          # 设置网格颜色
        self.colorGrid = color

    def setTextColor(self, color):          # 设置网格颜色
        self.colorText = color

    def setMousePassive(self, x, y):
        drawFlag = 0
        self.movePointX = x                  # 记录鼠标X坐标
        self.movePointY = y                  # 记录鼠标Y坐标
        return drawFlag

    def setMouseMove(self, x, y):
        drawFlag = 0
        self.movePointX = x                  # 记录鼠标X坐标
        self.movePointY = y                  # 记录鼠标Y坐标
        if self.moveState == True:
            drawFlag = 1
        self.getChoice()
        return drawFlag

    def setMouseClick(self, key, state):
        drawFlag = 0
        if key == 0 and state == 0:
            self.moveState = True
            if self.movePointX < self.size.x or self.movePointX > self.size.w + self.size.x: 
                self.moveState = False
            if self.movePointY < self.size.y or self.movePointY > self.size.y + self.size.h: 
                self.moveState = False
            if self.moveState == True:
                drawFlag = 1
        self.getChoice()
        return drawFlag

    def getChoice(self):
        # 选择指示器
        indicPointX = self.movePointX - self.size.x - self.margin.left
        indicWidth = self.size.w - self.margin.left - self.margin.right

        if self.moveState and indicPointX >= 0 and indicPointX <= indicWidth:
            self.clicked = 1
            self.choice = int(indicPointX * self.index.length / indicWidth) + self.index.begin
        else:
            self.clicked = 0
            return

        if self.choiceLast != self.choice:
            self.choiceLast = self.choice
            if self.call is not None:
                self.call(self.choice)

    def getCliceked(self):
        return self.clicked

    # 获取数据颜色
    def getAutoColor(self, a, b):
        if a > b : return (1.0, 0.0, 0.0, 1.0)     # 红色
        if a < b : return (0.0, 1.0, 0.0, 1.0)     # 绿色
        else : return (0.0, 0.5, 1.0, 1.0)         # 蓝色

    @abstractmethod
    def onGetColor(self, index, id = 0):
        return (1.0, 1.0, 1.0, 0.5)

    @abstractmethod
    def onGetValue(self, index, id = 0):
        return 0.0

    @abstractmethod
    def onGetList(self, index):
        return None

    @abstractmethod
    def onGetListColor(index, id = 0, sel = 0):
        return (1.0, 1.0, 1.0, 0.5)

    @abstractmethod
    def onGetScale(self, index):
        return dt.datetime.now().strftime('%Y-%m-%d')

    def drawInit(self):
        self._left   = self.margin.left / self.size.w
        self._right  = (self.size.w - self.margin.right) / self.size.w
        self._top    = (self.size.h - self.margin.top) / self.size.h
        self._bottom = self.margin.bottom / self.size.h

        self._num = self.index.end - self.index.begin + 1                                             # 计算箱体数量
        self._uint = (self._right - self._left) / (5 * self.index.length + 1)                         # 计算空白间隙
        self._uintPx = int((self.size.w - self.margin.left - self.margin.right) / self.index.length)  # 计算箱体像素

    def drawMargin(self):                   # 绘制坐标
        # 绘制边框
        glColor4fv(self.colorMargin)
        glBegin(GL_LINES)
        glVertex2f(self._left, self._top)
        glVertex2f(self._left, self._bottom)
        glVertex2f(self._right, self._top)
        glVertex2f(self._right, self._bottom)
        glVertex2f(self._left, self._top)
        glVertex2f(self._right, self._top)
        glVertex2f(self._left, self._bottom)
        glVertex2f(self._right, self._bottom)
        glEnd()

        # 绘制网格 等比
        glColor4fv(self.colorGrid)
        glLineStipple(2, 0x5555)
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINES)
        if self.row > 0 :
            marginRow = (self._right - self._left) / self.row
            for i in range(1, self.row):
                glVertex2f(self._left + marginRow * i, self._top)
                glVertex2f(self._left + marginRow * i, self._bottom)
        if self.col > 0 : 
            marginCol = (self._top - self._bottom) / self.col
            for i in range(1, self.col):
                glVertex2f(self._left, self._bottom + marginCol * i)
                glVertex2f(self._right, self._bottom + marginCol * i)
        glEnd()
        glDisable(GL_LINE_STIPPLE)

        # 绘制坐标标签
        if self.col <= 0 : return
        for i in range(self.col + 1):
            val_y = (self.valMax - self.valMin) / self.col * i + self.valMin
            font = self.font.number(self.format % val_y, self.colorText)

            font_pw = font.shape[1]
            font_ph = font.shape[0]
            font_b = font_ph / self.size.h / 2.0
            
            rect_x = (self.size.w - self.margin.right + 2) / self.size.w
            rect_pw = self.margin.right - self.margin.left
            rect_w = rect_pw / self.size.w
            
            font_x = self.font.prec(rect_x + rect_w - ((font_pw + 6) / self.size.w))  # 右对齐
            # font_x = self.font.prec((self.size.w - self.margin.right + 6) / self.size.w)  # 左对齐
            if i == 0:
                font_y = self.font.prec((self._bottom + marginCol * i))
            elif i == self.col:
                font_y = self.font.prec((self._bottom + marginCol * i) - font_b - font_b)
            else:
                font_y = self.font.prec((self._bottom + marginCol * i) - font_b)
            self.font.draw(font, font_x, font_y, font_pw, font_ph)

    def __drawChoiceValue(self, val, x1, x2, x3, y1, y2, id):
        color = winConfig.get_color_uint(self.onGetColor(self.choice, id))
        font = self.font.number(self.format % val, color)
        font_pw = font.shape[1]
        font_ph = font.shape[0]

        rect_pw = self.margin.right - self.margin.left
        rect_ph = font_ph + 4
        rect_w = rect_pw / self.size.w
        rect_h = rect_ph / self.size.h

        rect_x = (self.size.w - self.margin.right + 2) / self.size.w
        rect_y = self._bottom + y2 - rect_h / 2.0

        if rect_y < self._bottom:
            rect_y = self._bottom

        if rect_y > self._top - rect_h:
            rect_y = self._top - rect_h

        rect_m = rect_y + rect_h / 2.0

        glColor4f(0.03, 0.03, 0.03, 0.7)
        glRectf(rect_x, rect_y, rect_x + rect_w, rect_y + rect_h)

        glColor4f(1.0, 1.0, 1.0, 0.2)
        glBegin(GL_LINE_STRIP)
        glVertex2f(rect_x, rect_y)
        glVertex2f(rect_x + rect_w, rect_y)
        glVertex2f(rect_x + rect_w, rect_y + rect_h)
        glVertex2f(rect_x, rect_y + rect_h)
        glVertex2f(rect_x, rect_y)
        glEnd()
        
        font_x = self.font.prec(rect_x + rect_w - (font_pw + 6) / self.size.w)  # 右对齐
        # font_x = (self.size.w - self.margin.right + 6) / self.size.w          # 左对齐
        font_y = (rect_m - font_ph / self.size.h / 2.0)
        self.font.draw(font, font_x, font_y, font_pw, font_ph)

    def __drawChoiceList(self, list, x1, x2, x3, y1, y2, id):
        if len(list) < 5 : return

        rect_pw = self.margin.right - self.margin.left
        rect_ph = self.fontLabel[0].shape[0] * 10 + 22
        rect_w = rect_pw / self.size.w
        rect_h = rect_ph / self.size.h

        rect_x = (self.size.w - self.margin.right + 2) / self.size.w
        rect_y = self._bottom + y2 - rect_h / 2.0

        if rect_y < self._bottom:
            rect_y = self._bottom

        if rect_y > self._top - rect_h:
            rect_y = self._top - rect_h

        rect_m = rect_y + rect_h / 2.0

        glColor4f(0.03, 0.03, 0.03, 0.7)
        glRectf(rect_x, rect_y, rect_x + rect_w, rect_y + rect_h)

        glColor4f(1.0, 1.0, 1.0, 0.2)
        glBegin(GL_LINE_STRIP)
        glVertex2f(rect_x, rect_y)
        glVertex2f(rect_x + rect_w, rect_y)
        glVertex2f(rect_x + rect_w, rect_y + rect_h)
        glVertex2f(rect_x, rect_y + rect_h)
        glVertex2f(rect_x, rect_y)
        glEnd()

        glColor4f(1.0, 1.0, 1.0, 1.0)
        font_h = (self.fontLabel[0].shape[0] + 2) / self.size.h 
        for i in range(len(list)):
            font_x = (self.size.w - self.margin.right + 6) / self.size.w          # 左对齐
            font_y = (rect_y + rect_h) - font_h - font_h * i * 2
            font_pw = self.fontLabel[i].shape[1]
            font_ph = self.fontLabel[i].shape[0]
            # self.font.draw(self.fontLabel[i], font_x, font_y, font_pw, font_ph)
            self.font.drawTexture(self.fontLabelTid[i], font_x, font_y, font_pw, font_ph, self.size)
            
            color = winConfig.get_color_uint(self.onGetListColor(self.choice, id, i))
            if i == 4:
                font = self.font.number('%.02f%%' % list[i], color)
            else:
                font = self.font.number(self.format % list[i], color)

            font_pw = font.shape[1]
            font_ph = font.shape[0]
            font_x = self.font.prec(rect_x + rect_w - (font_pw + 6) / self.size.w)
            font_y = (rect_y + rect_h) - font_h * 2 - font_h * i * 2
            self.font.draw(font, font_x, font_y, font_pw, font_ph)

    def drawChoice(self, id = 0):
        if self.choice < self.index.begin : return 
        if self.choice > self.index.end : return 

        val = self.onGetValue(self.choice, id)
        x1 = self._uint * 5 * (self.choice - self.index.begin) + self._uint
        x2 = self._uint * 3 + x1
        x3 = (x2 - x1) / 2 + x1
        y1 = 0.00
        y2 = (val - self.valMin) / (self.valMax - self.valMin) * (self._top - self._bottom)

        # 绘制时间指示光标
        glColor4f(1.0, 1.0, 1.0, 0.1)
        if self._uintPx >= 5 :
            glRectf(self._left + x1, self._top, self._left + x2, self._bottom)
        else:
            glBegin(GL_LINES)
            glVertex2f(self._left + x3, self._top)
            glVertex2f(self._left + x3, self._bottom)
            glEnd()

        # 绘制值指示光标
        glColor4f(1.0, 1.0, 1.0, 0.2)
        glBegin(GL_LINES)
        glVertex2f(self._left + x3, self._bottom + y2)
        glVertex2f(self._right, self._bottom + y2)
        glEnd()
        
        # 绘制值指示面板
        
        list = self.onGetList(self.choice)
        if list is None:
            self.__drawChoiceValue(val, x1, x2, x3, y1, y2, id)
        else:
            self.__drawChoiceList(list, x1, x2, x3, y1, y2, id)
        
    # 绘制时标
    def drawScale(self, textBegin, tidBegin, textEnd, tidEnd):
        glColor4fv(self.colorText)
        # 起始日期
        if textBegin is not None:
            font_w = textBegin.shape[1]     # 文本宽度
            font_h = textBegin.shape[0]     # 文本高度
            font_x = self.font.prec(self.margin.left / self.size.w)
            font_y = self.font.prec((self.margin.bottom - font_h) / 2.0 / self.size.h)
            self.font.drawTexture(tidBegin, font_x, font_y, font_w, font_h, self.size)
            
        # 终止日期
        if textEnd is not None:
            font_w = textEnd.shape[1]     # 文本宽度
            font_h = textEnd.shape[0]     # 文本高度
            font_x = self.font.prec((self.size.w - self.margin.right - font_w) / self.size.w)
            font_y = self.font.prec((self.margin.bottom - font_h) / 2.0 / self.size.h)
            self.font.drawTexture(tidEnd, font_x, font_y, font_w, font_h, self.size)

        if self.choice < self.index.begin : return 
        if self.choice > self.index.end : return 

        x1 = self._uint * 5 * (self.choice - self.index.begin) + self._uint
        x2 = self._uint * 3 + x1
        x3 = (x2 - x1) / 2 + x1

        glColor4f(1.0, 1.0, 1.0, 0.1)

        font = self.font.number(self.onGetScale(self.choice), self.colorWhite)
        font_pw = font.shape[1]
        font_ph = font.shape[0]
        
        rect_pw = font_pw + 10
        rect_ph = 20
        rect_w = rect_pw / self.size.w
        rect_h = rect_ph / self.size.h
        rect_x = self._left + x3 - (rect_pw / 2.0) / self.size.w
        rect_y = (self.margin.bottom - rect_ph) / 2.0 / self.size.h

        limit_l = self.margin.left / self.size.w
        limit_r = (self.size.w - self.margin.right - rect_pw) / self.size.w
        
        if rect_x < limit_l : rect_x = limit_l
        if rect_x > limit_r : rect_x = limit_r
        font_x = rect_x + (rect_w / 2.0)- (font_pw / self.size.w / 2.0)
        font_y = rect_y + (rect_h / 2.0)- (font_ph / self.size.h / 2.0)

        glColor4f(0.03, 0.03, 0.03, 1.0)
        glRectf(rect_x, rect_y, rect_x + rect_w, rect_y + rect_h)
        glColor4f(1.0, 1.0, 1.0, 0.1)
        glBegin(GL_LINE_STRIP)
        glVertex2f(rect_x, rect_y)
        glVertex2f(rect_x, rect_y + rect_h)
        glVertex2f(rect_x + rect_w, rect_y + rect_h)
        glVertex2f(rect_x + rect_w, rect_y)
        glVertex2f(rect_x, rect_y)
        glEnd()
        self.font.draw(font, font_x, font_y, font_pw, font_ph)

    # 绘制柱形图
    def drawCurveCloumn(self, data, id = 0):
        if data is None : return
        for i in range(self._num):
            
            glColor4fv(self.onGetColor(i + self.index.begin, id))
            x1 = self._uint * 5 * i + self._uint
            x2 = self._uint * 3 + x1
            y1 = (0.0 - self.valMin) / (self.valMax - self.valMin) * (self._top - self._bottom)
            y2 = (data[i + self.index.begin] - self.valMin) / (self.valMax - self.valMin) * (self._top - self._bottom)
            
            if self._uintPx >= 5:                                                     # 大于5个像素则可以绘制K线
                glRectf(self._left + x1, self._bottom + y1, self._left + x2, self._bottom + y2)
            else:
                x3 = (x2 - x1) / 2 + x1
                
                glBegin(GL_LINES)
                glVertex2f(self._left + x3, self._bottom + y1)
                glVertex2f(self._left + x3, self._bottom + y2)
                glEnd()

    # 绘制折线图
    def drawCurveLine(self, data, id = 0):
        if data is None : return
        glBegin(GL_LINE_STRIP)
        start = False
        for i in range(self._num):
            if data[i + self.index.begin] == 0 and start is False : continue
            glColor4fv(self.onGetColor(i + self.index.begin, id))
            x1 = self._uint * 5 * i + self._uint
            x2 = self._uint * 3 + x1
            x = (x2 - x1) / 2 + x1
            y = (data[i + self.index.begin] - self.valMin) / (self.valMax - self.valMin) * (self._top - self._bottom)
            glVertex2f(self._left + x, self._bottom + y)
            start = True
        glEnd()

    # 绘制蜡烛图
    def drawCurveCandle(self, data):
        if data is None : return
        for i in range(self._num):

            glColor4fv(self.onGetColor(i + self.index.begin))

            x1 = self._uint * 5 * i + self._uint
            x2 = self._uint * 3 + x1
            y1 = (data[i + self.index.begin][0] - self.valMin) / (self.valMax - self.valMin) * (self._top - self._bottom)
            y2 = (data[i + self.index.begin][1] - self.valMin) / (self.valMax - self.valMin) * (self._top - self._bottom)
            
            pxh = 1 / self.size.h
            if y1 >= y2 and (y1 - y2) < pxh:
                y1 = y1 + pxh
            if y2 > y1 and (y2 - y1) < pxh:
                y2 = y2 + pxh

            if self._uintPx >= 5:                                                     # 大于5个像素则可以绘制K线
                glRectf(self._left + x1, self._bottom + y1, self._left + x2, self._bottom + y2)

            x3 = (x2 - x1) / 2 + x1
            y3 = (data[i + self.index.begin][2] - self.valMin) / (self.valMax - self.valMin) * (self._top - self._bottom)
            y4 = (data[i + self.index.begin][3] - self.valMin) / (self.valMax - self.valMin) * (self._top - self._bottom)

            glBegin(GL_LINES)
            glVertex2f(self._left + x3, self._bottom + y3)
            glVertex2f(self._left + x3, self._bottom + y4)
            glEnd()