from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from pack_graph import graphSize

class graphFrame(object):

    def __init__(self, winconf):
        self.winconf = winconf
        self.margin = winconf.get('Margin')
        self.listwidth = winconf.get('ListWidth')

    def update(self):
        # 区域A坐标 选择列表
        self.a = graphSize.rect()
        self.a.x = self.margin
        self.a.y = self.margin
        self.a.w = self.listwidth
        self.a.h = self.winconf.get_wsize_h() - self.margin * 2

        # 区域B坐标 扩展指标选择
        self.b = graphSize.rect()
        self.b.x = self.a.x + self.a.w
        self.b.y = self.a.y
        self.b.w = self.winconf.get_wsize_w() - self.a.w - self.margin * 2
        self.b.h = 20

        # 区域C坐标 时间轴
        self.c = graphSize.rect()
        self.c.x = self.b.x
        self.c.y = self.b.y + self.b.h
        self.c.w = self.b.w
        self.c.h = 35

        # 区域D坐标 扩展指标显示
        self.d = graphSize.rect()
        self.d.x = self.c.x
        self.d.y = self.c.y + self.c.h
        self.d.w = self.b.w
        self.d.h = int((self.winconf.get_wsize_h() - self.margin * 2 - 115) * 0.20)

        # 区域E坐标 扩展参数标签
        self.e = graphSize.rect()
        self.e.x = self.d.x
        self.e.y = self.d.y + self.d.h
        self.e.w = self.d.w
        self.e.h = 20

        # 区域F坐标 成交量显示
        self.f = graphSize.rect()
        self.f.x = self.e.x
        self.f.y = self.e.y + self.e.h
        self.f.w = self.e.w
        self.f.h = self.d.h

        # 区域G坐标 成交量标签
        self.g = graphSize.rect()
        self.g.x = self.f.x
        self.g.y = self.f.y + self.f.h
        self.g.w = self.f.w
        self.g.h = 20

        # 区域H坐标 K线图形显示
        self.h = graphSize.rect()
        self.h.x = self.g.x
        self.h.y = self.g.y + self.g.h
        self.h.w = self.g.w
        self.h.h = int((self.winconf.get_wsize_h() - self.margin * 2 - 115) * 0.60)

        # 区域I坐标 K线数据标签
        self.i = graphSize.rect()
        self.i.x = self.h.x
        self.i.y = self.h.y + self.h.h
        self.i.w = self.h.w
        self.i.h = self.winconf.get_wsize_h() - self.margin * 2 - self.b.h - self.c.h - self.d.h - self.e.h - self.f.h - self.g.h - self.h.h

    def set_frame(self, rect, color):       # 区域绘制
        glViewport(rect.x, rect.y, rect.w, rect.h)
        glColor4fv(color)
        glRecti(0, 0, 1, 1)

    def get_region_A(self):
        return self.a

    def set_region_A(self):     # 区域A坐标 选择列表
        self.set_frame(self.a, self.winconf.get_bcolor_list())

    def get_region_B(self):
        return self.b

    def set_region_B(self):     # 区域B坐标 扩展指标选择
        self.set_frame(self.b, self.winconf.get_bcolor_label()) 

    def get_region_C(self):
        return self.c

    def set_region_C(self):     # 区域C坐标 时间轴
        self.set_frame(self.c, self.winconf.get_bcolor_tline()) 

    def get_region_D(self):
        return self.d

    def set_region_D(self):     # 区域D坐标 扩展指标显示
        self.set_frame(self.d, self.winconf.get_bcolor_graph()) 

    def get_region_E(self):
        return self.e

    def set_region_E(self):     # 区域E坐标 扩展参数标签
        self.set_frame(self.e, self.winconf.get_bcolor_label()) 

    def get_region_F(self):
        return self.f

    def set_region_F(self):     # 区域F坐标 成交量显示
        self.set_frame(self.f, self.winconf.get_bcolor_graph()) 

    def get_region_G(self):
        return self.g

    def set_region_G(self):     # 区域G坐标 成交量标签
        self.set_frame(self.g, self.winconf.get_bcolor_label()) 

    def get_region_H(self):
        return self.h

    def set_region_H(self):     # 区域H坐标 K线图形显示
        self.set_frame(self.h, self.winconf.get_bcolor_graph()) 

    def get_region_I(self):
        return self.i

    def set_region_I(self):     # 区域I坐标 K线数据标签
        self.set_frame(self.i, self.winconf.get_bcolor_label()) 