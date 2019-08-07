from OpenGL.GL import *

from pack_graph import graphSize
from pack_graph import graphFont

class graphButton(object):
    def __init__(self, id, text, textfont, textcolor, backcolor, textway, clickcall):
        self.id = id
        self.text = text
        self.font = textfont
        self.way = textway
        self.clickcall = clickcall

        self.rect = None
        self.absrect = None
        self.color = backcolor
        self.check = False
        self.mouseKey = 0
        self.mouseState = 1
        self.mousePassive = False
        self.mouseLastPassive = False
        
        self.font.setSpace(1)
        self.label = self.font.string(text, textcolor)
        self.labelTid = self.font.getTexture(self.label)

    def setSize(self, x, y, width, height, frect):
        self.frect = frect
        self.rect = graphSize.rectEx(x, y, width, height, frect)

    def setCheck(self, check):
        self.check = check

    def setMouseCheck(self, key, state):
        self.mouseKey = key
        self.mouseState = state
        if state == 0 and self.mousePassive == True :     # 按钮触发事件
            self.clickcall(self.id)

    def setMousePassive(self, x, y):
        drawFlag = 0
        self.mousePassive = True
        self.mouseKey = 0
        self.mouseState = 1

        if self.absrect == None:
            self.mousePassive = False
            return drawFlag

        if x < self.absrect.x :
            self.mousePassive = False
        if x > self.absrect.x + self.absrect.w :
            self.mousePassive = False
        if y < self.absrect.y :
            self.mousePassive = False
        if y > self.absrect.y + self.absrect.h :
            self.mousePassive = False
        
        if self.mouseLastPassive != self.mousePassive :
            self.mouseLastPassive = self.mousePassive
            drawFlag = 1
        return drawFlag

    def draw(self):
        abs_x = self.frect.x + self.rect.x                                          # 计算绝对坐标值 X
        abs_y = self.frect.h + self.frect.y - self.rect.y - self.rect.h             # 计算绝对坐标值 Y  

        self.absrect = graphSize.rect(int(abs_x), int(abs_y), int(self.rect.w), int(self.rect.h))
        glViewport(self.absrect.x, self.absrect.y, self.absrect.w, self.absrect.h)  # 转换坐标 按钮内部坐标

        # 鼠标滑过检测
        if self.mousePassive == True:                   
            if self.mouseKey == 0 and self.mouseState == 0:
                glColor4f(self.color[0], self.color[1], self.color[2], self.color[3] + 0.4)
            else:
                glColor4f(self.color[0], self.color[1], self.color[2], self.color[3] + 0.2)
        else:
            if self.check == True:
                glColor4f(self.color[0], self.color[1], self.color[2], self.color[3] + 0.15)
            else: 
                glColor4fv(self.color)                  # 设置按钮背景色
        
        glRectf(0, 0, 1, 1)                             # 绘制按钮    

        font_w = self.label.shape[1]                    # 文本宽度
        font_h = self.label.shape[0]                    # 文本高度

        font_pw = font_w / self.rect.w
        font_ph = font_h / self.rect.h

        font_px = int((1 - font_pw) / 2 * 100) / 100.0  # 文本绘制横轴坐标  默认居中
        font_py = int((1 - font_ph) / 2 * 100) / 100.0  # 文本绘制纵轴坐标  

        if self.way == graphFont.Left :
            font_px = 0.05                              # 文本绘制横轴坐标  左对齐
        if self.way == graphFont.Right :
            font_px = 0.95 - ffont_pw                   # 文本绘制横轴坐标  右对齐

        glColor4f(255, 255, 255, 255)
        self.font.drawTexture(self.labelTid, font_px, font_py, font_w, font_h, self.rect)

        glViewport(self.frect.x, self.frect.y, self.frect.w, self.frect.h)      # 还原坐标系
