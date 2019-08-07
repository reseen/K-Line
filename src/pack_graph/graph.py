from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from . import winConfig  as winconf
from . import winTools   as wintool

from . import graphFont as gpFont
from . import graphFrame as gpFrame
from . import graphSize as gpSize
from . import graphButton as gpButton
from . import graphLabel as gpLabel
from . import graphKli as gpKli
from . import graphVol as gpVol
from . import graphPrm as gpPrm
from . import graphTmb as gpTmb

import time

class graph():

    def __init__(self, dataList, normList, onGetData, onGetNorm):
        self.dataList = dataList
        self.normList = normList
        self.onGetData = onGetData
        self.onGetNorm = onGetNorm
        self.data = None
        self.norm = None
        self.m_wcf = None
        self.m_wts = None
        self.m_gpFont = None
        self.m_gpTextFont = None
        self.m_gpFrame = None
        self.dataButton = []    # 数据按钮
        self.dataLabel = []     # 数据标签
        self.normButton = []    # 指标按钮
        self.normLabel = []     # 指标标签
        self.kli = None         # K线面板
        self.vol = None         # 成交量面板
        self.nrm = None         # 指标面板
        self.tmb = None

    # 窗口尺寸发生变化
    def ReshapeFunc(self, width, height):
        set = False  
        if width < self.m_wcf.get('Min-Width'):
            width = self.m_wcf.get('Min-Width')
            set = True
        if height < self.m_wcf.get('Min-Height'):
            height = self.m_wcf.get('Min-Height')
            set = True

        if set is True:
            glutReshapeWindow(width, height)
        self.m_wcf.set_wsize(width, height)

    # 窗口重绘
    def drawFunc(self):
        get_now_milli_time = lambda : int(time.time() * 1000)
        time_start = get_now_milli_time()

        glClear(GL_COLOR_BUFFER_BIT)
        self.m_gpFrame.update()

        self.m_gpFrame.set_region_A()    # 列表
        for i in range(len(self.dataButton)):
            self.dataButton[i].setSize(0, i * 26, 1, 25, self.m_gpFrame.get_region_A())
            self.dataButton[i].draw()

        self.m_gpFrame.set_region_B()    # 参数选择
        for i in range(len(self.normButton)):
            self.normButton[i].setSize(i * 60, 0.0, 59, 1.0, self.m_gpFrame.get_region_B())
            self.normButton[i].draw()

        self.m_gpFrame.set_region_C()    # 时间轴
        self.tmb.setSize(self.m_gpFrame.get_region_C())
        self.tmb.draw()

        self.m_gpFrame.set_region_D()    # 扩展参数图像
        self.prm.setSize(self.m_gpFrame.get_region_D())
        self.prm.draw()

        self.m_gpFrame.set_region_E()    # 扩展参数标签

        self.m_gpFrame.set_region_F()    # 成交量图像
        self.vol.setSize(self.m_gpFrame.get_region_F())
        self.vol.draw()

        self.m_gpFrame.set_region_G()    # 成交量标签
        self.dataLabel[5].setSize(10, 0.1, 80, 0.9, self.m_gpFrame.get_region_G())
        self.dataLabel[5].draw()

        self.m_gpFrame.set_region_H()    # K线图形区域
        self.kli.setSize(self.m_gpFrame.get_region_H())
        self.kli.draw()

        self.m_gpFrame.set_region_I()    # K线数据标签
        for i in range(4):
            self.dataLabel[i].setSize(i * 80 + 10, 0.1, 50, 0.9, self.m_gpFrame.get_region_I())
            self.dataLabel[i].draw()

        glutSwapBuffers()

        print('draw time: %d' % int(get_now_milli_time() - time_start))

    # 鼠标点击
    def mouseClick(self, key, state, x, y):
        for item in self.dataButton:
            item.setMouseCheck(key, state)
        for item in self.normButton:
            item.setMouseCheck(key, state)

        self.tmb.setMouseClick(key, state)
        self.kli.setMouseClick(key, state)
        self.vol.setMouseClick(key, state)

        clicked = 0
        clicked += self.kli.getCliceked()
        clicked += self.vol.getCliceked()

        if clicked == 0:
            self.kli.setChoice(-1)
            self.vol.setChoice(-1)

        if state == 0 : self.drawFunc()

    # 鼠标按下移动
    def mouseMove(self, x, y):
        drawFlag = 0
        drawFlag |= self.tmb.setMouseMove(x, self.m_wcf.get_wsize_h() - y)
        drawFlag |= self.kli.setMouseMove(x, self.m_wcf.get_wsize_h() - y)
        drawFlag |= self.vol.setMouseMove(x, self.m_wcf.get_wsize_h() - y)
        if drawFlag != 0 : self.drawFunc()
        # print("mouseMove x = %d, y = %d" % (x, y))

    # 鼠标抬起移动
    def mousePassive(self, x, y):
        drawFlag = 0
        for item in self.dataButton:
            drawFlag |= item.setMousePassive(x, self.m_wcf.get_wsize_h() - y)
        for item in self.normButton:
            drawFlag |= item.setMousePassive(x, self.m_wcf.get_wsize_h() - y)
        drawFlag |= self.tmb.setMousePassive(x, self.m_wcf.get_wsize_h() - y)
        drawFlag |= self.kli.setMousePassive(x, self.m_wcf.get_wsize_h() - y)
        drawFlag |= self.vol.setMousePassive(x, self.m_wcf.get_wsize_h() - y)

        if drawFlag != 0 : self.drawFunc()
        # print("mousePassive x = %d, y = %d" % (x, y))

    # 鼠标脱离窗口
    def mouseEntry(self, state):
        pass
        # print("mouseEntry state = %d" % state)

    # 键盘按键响应
    def keyboard(self, key, x, y):
        if key == b'\x1b' or key == b'q':        # Esc is 27
            sys.exit()

    def onDataButton(self, id):
        self.data = self.onGetData(self.dataList[id][0])
        self.kli.setData(self.data)
        self.vol.setData(self.data)
        self.tmb.setData(self.data)

        for i in range(len(self.dataButton)):
            self.dataButton[i].setCheck(True if i == id else False)
    
        print("read data %s[%s] success!" % (self.dataList[id][1], self.dataList[id][0]))

    def onNormButton(self, id):
        self.norm = self.onGetNorm(self.normList[id], self.data)
        self.prm.setData(self.norm)

        for i in range(len(self.normButton)):
            self.normButton[i].setCheck(True if i == id else False)  

    def onTmb(self, begin, end, length):
        self.kli.setIndex(begin, end, length)
        self.vol.setIndex(begin, end, length)
        self.prm.setIndex(begin, end, length)

    def onKli(self, choice):
        if self.data is None : return
        if choice >= len(self.data) : return 
        if choice == 0:
            if self.data[choice][1] == 0 :
                perc = 100.00
            else:
                perc = (self.data[choice][2] - self.data[choice][1]) / self.data[choice][1] * 100.00
        else:
            perc = (self.data[choice][2] - self.data[choice - 1][2]) / self.data[choice - 1][2] * 100.00
        self.dataLabel[0].setValue(self.data[choice][1], '%.02f')
        self.dataLabel[1].setValue(self.data[choice][2], '%.02f')
        self.dataLabel[2].setValue(self.data[choice][3], '%.02f')
        self.dataLabel[3].setValue(self.data[choice][4], '%.02f')
        self.dataLabel[4].setValue(perc, "%.02f%%")
        self.dataLabel[5].setValue(self.data[choice][5], '%d')

        self.vol.setChoice(choice)

    def onVol(self, choice):
        if self.data is None : return
        if choice >= len(self.data) : return 
        if choice == 0:
            if self.data[choice][1] == 0 :
                perc = 100.00
            else:
                perc = (self.data[choice][2] - self.data[choice][1]) / self.data[choice][1] * 100.00
        else:
            perc = (self.data[choice][2] - self.data[choice - 1][2]) / self.data[choice - 1][2] * 100.00
        self.dataLabel[0].setValue(self.data[choice][1], '%.02f')
        self.dataLabel[1].setValue(self.data[choice][2], '%.02f')
        self.dataLabel[2].setValue(self.data[choice][3], '%.02f')
        self.dataLabel[3].setValue(self.data[choice][4], '%.02f')
        self.dataLabel[4].setValue(perc, "%.02f%%")
        self.dataLabel[5].setValue(self.data[choice][5], '%d')

        self.kli.setChoice(choice)

    def onPrm(self, choice):
        pass

    def show(self):
        self.m_wcf = winconf.winConfig()                            # 初始化配置文件类
        self.m_wts = wintool.winTools(self.m_wcf.get_appname())     # 初始化窗口工具类
        self.m_wts.set_appID()                                      # 重设置窗口AppID

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
        glutInitWindowSize(self.m_wcf.get_wsize_w(), self.m_wcf.get_wsize_h())
        glutCreateWindow(self.m_wcf.get_appname())

        self.m_gpFrame = gpFrame.graphFrame(self.m_wcf)

        glEnable(GL_BLEND)                           # 启用半透明
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glutReshapeFunc(self.ReshapeFunc)            # 窗口变化响应
        glutDisplayFunc(self.drawFunc)               # 绘图控制
        glutKeyboardFunc(self.keyboard)              # 键盘响应
        glutMouseFunc(self.mouseClick)               # 鼠标响应
        glutMotionFunc(self.mouseMove)               # 鼠标按下移动
        glutPassiveMotionFunc(self.mousePassive)     # 鼠标松开移动
        glutEntryFunc(self.mouseEntry)               # 鼠标离开窗口
        gluOrtho2D(0, 1, 0, 1)                       # 设置坐标系
        glClearColor(0.0, 0.0, 0.0, 1.0)             # 清除背景颜色

        self.m_wts.set_icon(self.m_wcf.get('AppIcon'))
        self.m_gpFont = gpFont.graphFont(self.m_wcf.get('CnFont'), 12, self.m_wcf.get('AppFontVector'))

        # 初始化字体与颜色
        font = self.m_gpFont
        colorFont = self.m_wcf.get_fcolor_button()
        colorBack = self.m_wcf.get_bcolor_button()

        # 添加列表按钮
        for i in range(len(self.dataList)):
            self.dataButton.append(gpButton.graphButton(i, self.dataList[i][1], self.m_gpFont, colorFont, colorBack, gpFont.Center, self.onDataButton))
        
        # 添加指标按钮
        for i in range(len(self.normList)):
            self.normButton.append(gpButton.graphButton(i, self.normList[i], self.m_gpFont, colorFont, colorBack, gpFont.Center, self.onNormButton))
        
        # 添加加标签
        self.dataLabel.append(gpLabel.graphLabel(0, 'O', self.m_gpFont, colorFont))
        self.dataLabel.append(gpLabel.graphLabel(1, 'C', self.m_gpFont, colorFont))
        self.dataLabel.append(gpLabel.graphLabel(2, 'H', self.m_gpFont, colorFont))
        self.dataLabel.append(gpLabel.graphLabel(3, 'L', self.m_gpFont, colorFont))
        self.dataLabel.append(gpLabel.graphLabel(4, 'P', self.m_gpFont, colorFont))
        self.dataLabel.append(gpLabel.graphLabel(5, 'VOL', self.m_gpFont, colorFont))

        # 添加K线面板
        self.kli = gpKli.graphKline(self.m_gpFont, self.onKli)
        self.vol = gpVol.graphVolume(self.m_gpFont, self.onVol)
        self.prm = gpPrm.graphParam(self.m_gpFont, self.onPrm)
        self.tmb = gpTmb.graphTimebar(self.onTmb)

        glutMainLoop()

if __name__ == "__main__":
    gp = graph()
    gp.show()