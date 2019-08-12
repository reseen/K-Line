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

    def __init__(self, dataList, normList, onGetData, onGetNorm, onGetDataEx):
        self.dataList = dataList
        self.normList = normList
        self.onGetData = onGetData
        self.onGetNorm = onGetNorm
        self.onGetDataEx = onGetDataEx
        self.data = None
        self.norm = None
        self.m_wcf = None
        self.m_wts = None
        self.m_gpFont = None
        self.m_gpTextFont = None
        self.m_gpFrame = None
        self.dataButton = []    # 数据按钮
        self.dataLabel = []     # 数据标签
        self.volLabel = []      # 成交量标签
        self.normButton = []    # 指标按钮
        self.normLabel = []     # 指标标签
        self.kli = None         # K线面板
        self.vol = None         # 成交量面板
        self.nrm = None         # 指标面板
        self.tmb = None         # 时间轴面板

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
        for i in range(len(self.normLabel)):
            self.normLabel[i].setSize(i * 100 + 10, 0.1, 70, 0.9, self.m_gpFrame.get_region_E())
            self.normLabel[i].draw()

        self.m_gpFrame.set_region_F()    # 成交量图像
        self.vol.setSize(self.m_gpFrame.get_region_F())
        self.vol.draw()

        self.m_gpFrame.set_region_G()    # 成交量标签
        for i in range(len(self.volLabel)):
            self.volLabel[i].setSize(i * 100 + 10, 0.1, 70, 0.9, self.m_gpFrame.get_region_G())
            self.volLabel[i].draw()

        self.m_gpFrame.set_region_H()    # K线图形区域
        self.kli.setSize(self.m_gpFrame.get_region_H())
        self.kli.draw()

        self.m_gpFrame.set_region_I()    # K线数据标签
        for i in range(len(self.dataLabel)):
            self.dataLabel[i].setSize(i * 100 + 10, 0.1, 70, 0.9, self.m_gpFrame.get_region_I())
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
        self.prm.setMouseClick(key, state)

        clicked = 0
        clicked += self.kli.getCliceked()
        clicked += self.vol.getCliceked()
        clicked += self.prm.getCliceked()
        if clicked == 0:
            self.kli.setChoice(-1)
            self.vol.setChoice(-1)
            self.prm.setChoice(-1)

        if state == 0 : self.drawFunc()

    # 鼠标按下移动
    def mouseMove(self, x, y):
        drawFlag = 0
        drawFlag |= self.tmb.setMouseMove(x, self.m_wcf.get_wsize_h() - y)
        drawFlag |= self.kli.setMouseMove(x, self.m_wcf.get_wsize_h() - y)
        drawFlag |= self.vol.setMouseMove(x, self.m_wcf.get_wsize_h() - y)
        drawFlag |= self.prm.setMouseMove(x, self.m_wcf.get_wsize_h() - y)
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
        drawFlag |= self.prm.setMousePassive(x, self.m_wcf.get_wsize_h() - y)

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

    # 数据选择按钮回调
    def onDataButton(self, id):
        self.data = self.onGetData(self.dataList[id][0])
        self.kli.setData(self.data)
        self.kli.setDataEx(self.onGetDataEx(0, self.data))
        self.vol.setData(self.data)
        self.vol.setDataEx(self.onGetDataEx(1, self.data))
        self.onNormButton(0)
        
        self.dataLabel = []
        for i in range(len(self.kli.dataEx)):
            self.dataLabel.append(gpLabel.graphLabel(i, self.kli.dataEx[i].label, self.m_gpFont, winconf.get_color_uint(self.kli.dataEx[i].color)))

        self.volLabel = []
        self.volLabel.append(gpLabel.graphLabel(i, 'VOL', self.m_gpFont, (255, 255, 255, 220)))
        for i in range(len(self.vol.dataEx)):
            self.volLabel.append(gpLabel.graphLabel(i, self.vol.dataEx[i].label, self.m_gpFont, winconf.get_color_uint(self.vol.dataEx[i].color)))

        for i in range(len(self.dataButton)):
            self.dataButton[i].setCheck(True if i == id else False)

    # 参数选择按钮回调
    def onNormButton(self, id):
        if self.data is None : return
        self.norm = self.onGetNorm(self.normList[id], self.data)
        self.prm.setData(self.norm)

        if self.norm is not None:
            self.normLabel = []
            for i in range(len(self.norm)):
                if self.norm[i].color is None:
                    self.normLabel.append(gpLabel.graphLabel(i, self.norm[i].label, self.m_gpFont, (255, 255, 255, 220)))
                else:
                    self.normLabel.append(gpLabel.graphLabel(i, self.norm[i].label, self.m_gpFont, winconf.get_color_uint(self.norm[i].color)))
            for i in range(len(self.normButton)):
                self.normButton[i].setCheck(True if i == id else False)

        self.tmb.setData(self.data)     # 最后设置TimeBar 确定选中区域
    
        # 设置标签值
    def setLabel(self, choice):
        if self.data is None : return

        for i in range(len(self.dataLabel)):
            self.dataLabel[i].setValue(self.kli.dataEx[i].value[choice], self.kli.dataEx[i].fmt, winconf.get_color_uint(self.kli.onGetColor(choice, i + self.kli.idEx)))
       
        for i in range(len(self.volLabel)):
            if i == 0:
                self.volLabel[i].setValue(self.vol.data[choice], '%d', winconf.get_color_uint(self.vol.onGetColor(choice, i)))
            else:
                self.volLabel[i].setValue(self.vol.dataEx[i - 1].value[choice], self.vol.dataEx[i - 1].fmt, winconf.get_color_uint(self.vol.onGetColor(choice, i + self.vol.idEx - 1)))

        for i in range(len(self.normLabel)):
            self.normLabel[i].setValue(self.norm[i].value[choice], self.norm[i].fmt, winconf.get_color_uint(self.prm.onGetColor(choice, i)))
    
    # 时间轴选择回调
    def onTmb(self, begin, end, length):
        self.kli.setIndex(begin, end, length)
        self.vol.setIndex(begin, end, length)
        self.prm.setIndex(begin, end, length)
    
    # K线面板动作回调函数
    def onKli(self, choice):
        self.setLabel(choice)
        self.vol.setChoice(choice)
        self.prm.setChoice(choice)

    # 成交量面板动作回调函数
    def onVol(self, choice):
        self.setLabel(choice)
        self.kli.setChoice(choice)
        self.prm.setChoice(choice)

    # 参数面板动作回调函数
    def onPrm(self, choice):
        self.setLabel(choice)
        self.kli.setChoice(choice)
        self.vol.setChoice(choice)

    def show(self):
        self.m_wcf = winconf.winConfig()                            # 初始化配置文件类
        self.m_wts = wintool.winTools(self.m_wcf.get_appname())     # 初始化窗口工具类
        self.m_wts.set_appID()                                      # 重设置窗口AppID

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
        glutInitWindowSize(self.m_wcf.get_wsize_w(), self.m_wcf.get_wsize_h())
        glutCreateWindow(self.m_wcf.get_appname())

        glEnable(GL_BLEND)                                          # 启用颜色混合
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)           # 启用半透明
        glutReshapeFunc(self.ReshapeFunc)                           # 窗口变化响应
        glutKeyboardFunc(self.keyboard)                             # 键盘响应
        glutMouseFunc(self.mouseClick)                              # 鼠标响应
        glutMotionFunc(self.mouseMove)                              # 鼠标按下移动
        glutPassiveMotionFunc(self.mousePassive)                    # 鼠标松开移动
        glutEntryFunc(self.mouseEntry)                              # 鼠标离开窗口
        glutDisplayFunc(self.drawFunc)                              # 绘图控制
        gluOrtho2D(0, 1, 0, 1)                                      # 设置坐标系
        glClearColor(0.0, 0.0, 0.0, 1.0)                            # 清除背景颜色

        self.m_wts.set_icon(self.m_wcf.get('AppIcon'))
        self.m_gpFont = gpFont.graphFont(self.m_wcf.get('CnFont'), 12, self.m_wcf.get('AppFontVector'))

        # 初始化字体与颜色
        font = self.m_gpFont
        colorFont = self.m_wcf.get_fcolor_button()
        colorBack = self.m_wcf.get_bcolor_button()

        # 创建主体框架
        self.m_gpFrame = gpFrame.graphFrame(self.m_wcf)

        # 添加列表按钮
        for i in range(len(self.dataList)):
            self.dataButton.append(gpButton.graphButton(i, self.dataList[i][1], self.m_gpFont, colorFont, colorBack, gpFont.Center, self.onDataButton))
        
        # 添加指标按钮
        for i in range(len(self.normList)):
            self.normButton.append(gpButton.graphButton(i, self.normList[i], self.m_gpFont, colorFont, colorBack, gpFont.Center, self.onNormButton))
        
        self.kli = gpKli.graphKline(self.m_gpFont, self.onKli)      # 添加K线面板
        self.vol = gpVol.graphVolume(self.m_gpFont, self.onVol)     # 添加成交量面板
        self.prm = gpPrm.graphParam(self.m_gpFont, self.onPrm)      # 创建参数面板
        self.tmb = gpTmb.graphTimebar(self.onTmb)                   # 创建时间选择面板

        glutMainLoop()

if __name__ == "__main__":
    gp = graph()
    gp.show()