from OpenGL.GL import *

from pack_graph import graphSize
import win32con
import win32gui
import win32api

MOVE_NONE  = 0
MOVE_LEFT  = 1
MOVE_RIGHT = 2
MOVE_ALL   = 3

class graphTimebar():
    def __init__(self, timebarFunc = None):
        self.ctrlbarWidth = 10          # 时间轴控制块宽度
        self.defChoice = 60             # 默认显示60个值
        self.minChoice = 20             # 最少显示20个值
        self.minWidth = None            # 20个值所对应的像素宽度
        self.pointLeft = 0.5            # 左侧指针
        self.pointRight = 1.0
        self.size = None
        self.mouseChange = False
        self.mouseChangeLast = False
        self.timebarFunc = timebarFunc

        self.data = None
        self.dataLen = 0

        self.moveState = 0              # 移动状态
        self.movePointX = 0             # 移动坐标
        self.movePointY = 0             # 移动坐标

    def setSize(self, fsize):
        self.size = fsize
        self.margin = self.ctrlbarWidth / self.size.w / 2

        self.x1 = self.pointLeft * (1.0 - self.ctrlbarWidth / self.size.w) + self.margin
        self.x2 = self.pointRight * (1.0 - self.ctrlbarWidth / self.size.w) + self.margin

        if self.minWidth == None : self.minWidth = self.margin * 3

    def setData(self, data):
        self.data = data
        self.dataLen = len(data)
        # 计算最小宽度
        self.minWidth = self.minChoice / self.dataLen * (self.size.w - self.margin * 2) / self.size.w        
        if self.minWidth < self.margin * 3 : self.minWidth = self.margin * 3
        if self.minWidth > 1.0 : self.minWidth = 1.0

        # 计算默认宽度
        defWidth = self.defChoice / self.dataLen * (self.size.w - self.margin * 2) / self.size.w
        if defWidth < self.minWidth : defWidth = self.minWidth
        if defWidth > 1.0 : defWidth = 1.0

        # 设置选择区域
        self.pointRight = 1.0
        self.pointLeft  = 1.0 - defWidth

        if self.timebarFunc != None: 
            self.timebarFunc(self.getPosLeft(), self.getPosRight(), self.getPosLength())

    def getPosLeft(self):
        return int(self.dataLen * self.pointLeft + 0.5)

    def getPosRight(self):
        right = int(self.dataLen * self.pointRight + 0.5) 
        if right >= self.dataLen:
             right = self.dataLen - 1
        return right

    def getPosLength(self):
        length = self.getPosRight() - self.getPosLeft() + 1
        if length < self.minChoice : length = self.minChoice
        return length

    def setMousePassive(self, x, y):
        drawFlag = 0
        self.movePointX = x                  # 记录鼠标X坐标
        self.movePointY = y                  # 记录鼠标Y坐标

        if self.size == None : return drawFlag
        if self.movePointX < self.size.x or self.movePointX > self.size.w + self.size.x : 
            if self.mouseChange == True:
                self.mouseChange = self.mouseChangeLast = False
                win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_ARROW))
                drawFlag = 1
            return drawFlag
        if self.movePointY < self.size.y or self.movePointY > self.size.y + self.size.h : 
            if self.mouseChange == True:
                self.mouseChange = self.mouseChangeLast = False
                win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_ARROW))
                drawFlag = 1
            return drawFlag

        pointX = (self.movePointX - self.size.x) / self.size.w

        if pointX > self.x1 - self.margin and  pointX < self.x1 + self.margin :     # 左侧调整鼠标变化
            win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_SIZEWE))
            self.mouseChange = True
        elif pointX > self.x2 - self.margin and  pointX < self.x2 + self.margin :   # 右侧调整鼠标变化
            win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_SIZEWE))
            self.mouseChange = True
        elif pointX > self.x1 + self.margin and  pointX < self.x2 - self.margin :   # 整体拖动鼠标变化
            win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_ARROW))
            self.mouseChange = True
        else:
            win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_ARROW))          # 鼠标还原
            self.mouseChange = False
        
        if self.mouseChangeLast != self.mouseChange :
            self.mouseChangeLast = self.mouseChange
            drawFlag = 1
        return drawFlag

    def setMouseClick(self, key, state):
        if self.size == None: 
            self.moveState = None
            return
        if self.movePointX < self.size.x or self.movePointX > self.size.w + self.size.x : 
            self.moveState = None
            return
        if self.movePointY < self.size.y or self.movePointY > self.size.y + self.size.h : 
            self.moveState = None
            return
        # 判断鼠标按下
        if key == 0 and state == 0:
            pointX = (self.movePointX - self.size.x) / self.size.w
            if pointX > self.x1 - self.margin and  pointX < self.x1 + self.margin:      # 左侧调整
                self.moveState = MOVE_LEFT
            elif pointX > self.x2 - self.margin and  pointX < self.x2 + self.margin:    # 右侧调整
                self.moveState = MOVE_RIGHT
            elif pointX > self.x1 + self.margin and  pointX < self.x2 - self.margin:    # 整体拖动
                self.moveState = MOVE_ALL
            else:
                self.moveState = MOVE_NONE
        # 判断鼠标松开
        if key == 0 and state == 1:
            self.moveState = MOVE_NONE

    def setMouseMove(self, x, y):
        drawFlag = 0
        if self.moveState == MOVE_NONE : 
            self.movePointX = x
            self.movePointY = y
            return drawFlag
            
        if self.movePointX != 0:
            range = (x - self.movePointX) / self.size.w
            # 判断左侧拖动
            if self.moveState == MOVE_LEFT:
                self.pointLeft = self.pointLeft + range
                if self.pointLeft <= 0.0: 
                    self.pointLeft = 0.0 
                if self.pointLeft >= self.pointRight - self.minWidth: 
                    self.pointLeft = self.pointRight - self.minWidth
                if self.timebarFunc != None: 
                    self.timebarFunc(self.getPosLeft(), self.getPosRight(), self.getPosLength())
                drawFlag = 1

            # 判断右侧拖动
            if self.moveState == MOVE_RIGHT:
                self.pointRight = self.pointRight + range
                if self.pointRight >= 1.0: 
                    self.pointRight = 1.0 
                if self.pointRight <= self.pointLeft + self.minWidth: 
                    self.pointRight = self.pointLeft + self.minWidth
                if self.timebarFunc != None: 
                    self.timebarFunc(self.getPosLeft(), self.getPosRight(), self.getPosLength())
                drawFlag = 1

            # 判断整体拖动
            if self.moveState == MOVE_ALL:
                self.pointLeft = self.pointLeft + range
                self.pointRight = self.pointRight + range

                if self.pointLeft < 0.0:
                    self.pointRight = self.pointRight - self.pointLeft
                    self.pointLeft = 0.0
                if self.pointRight > 1.0:
                    self.pointLeft = self.pointLeft - (self.pointRight - 1.0)
                    self.pointRight = 1.0
                if self.timebarFunc != None: 
                    self.timebarFunc(self.getPosLeft(), self.getPosRight(), self.getPosLength())
                drawFlag = 1

        # 记录鼠标坐标
        self.movePointX = x
        self.movePointY = y
        return drawFlag

    def draw(self):

        if self.data != None:
            valMax = 0.0
            valMin = 10000000.0

            for val in self.data:
                if valMax < val[1] : valMax = val[1]
                if valMax < val[2] : valMax = val[2]
                if valMax < val[3] : valMax = val[3]
                if valMin > val[1] : valMin = val[1]
                if valMin > val[2] : valMin = val[2]
                if valMin > val[4] : valMin = val[4]

            unitK = 1.0 / (valMax - valMin) * 0.8
            length = len(self.data)
            # 绘制开盘价格
            glColor4f(0.0, 1.0, 0.0, 0.4)
            glBegin(GL_LINE_STRIP)
            x = 0.0
            y = unitK * (self.data[0][1] - valMin) + 0.1
            glVertex2f(x, y)
            for i in range(1, length):
                x = (i + 1) / length
                y = unitK * (self.data[i][1] - valMin) + 0.1
                glVertex2f(x, y)
            glEnd()
            # 绘制收盘价格
            glColor4f(1.0, 0.0, 0.0, 0.4)
            glBegin(GL_LINE_STRIP)
            x = 0.0
            y = unitK * (self.data[0][2] - valMin) + 0.1
            glVertex2f(x, y)
            for i in range(1, length):
                x = (i + 1) / length
                y = unitK * (self.data[i][2] - valMin) + 0.1
                glVertex2f(x, y)
            glEnd()
        
        # 绘制选择框
        alpha = 0.1 if self.mouseChange else 0.0
            
        glColor4f(0.3, 0.3, 0.8, 0.5 + alpha)
        glRectf(self.x1 - self.margin, 0.0, self.x1 + self.margin, 1.0)
        glRectf(self.x2 - self.margin, 0.0, self.x2 + self.margin, 1.0)

        glColor4f(0.3, 0.3, 0.8, 0.15 + alpha)
        glRectf(self.x1 + self.margin, 0.0, self.x2 - self.margin, 1.0)