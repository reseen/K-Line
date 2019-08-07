import json


def get_color_uint(color):
    return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), int(color[3] * 255))

class winConfig(object):

    def __init__(self, path = '../data/kline.json'):

        self._wsize = {'Width':800, 'Height':480}               # 窗口默认大小

        self._bcolor_base  = (0, 0, 0, 255)                     # 基础色调
        self._bcolor_list  = (100, 100, 220, 30)                # 列表颜色
        self._bcolor_lable = (100, 100, 255, 40)                # 标签背景
        self._bcolor_tline = (100, 100, 255, 30)                # 时间轴背景
        self._bcolor_graph = (255, 255, 255, 10)                # 绘图板背景

        self._fcolor_button = (255, 255, 255, 255)              # 按钮文字色
        self._bcolor_button = (100, 100, 220, 40)               # 按钮背景色

        try:
            self._path = path
            with open(path, 'r', encoding = 'UTF-8') as f:      # 打开文件
                self._jconfig = json.loads(f.read())            # 读取文件
                self._wsize.update(Width = self._jconfig ['Def-Width'], Height = self._jconfig ['Def-Height'])
        except:
            print('配置文件"kline.json"不存在，请检查。')

    def get(self, label):
        return self._jconfig[label]

    def get_appname(self):
        return self.get('AppName')

    '''
    应用基础颜色配置
    '''
    def get_color_rgba(self, color):
        return (float(color[0]) / 255.0, float(color[1]) / 255.0, float(color[2]) / 255.0, float(color[3]) / 255.0)
    
    def get_bcolor_base(self):
        return self.get_color_rgba(self._bcolor_base)
        
    def get_bcolor_list(self):
        return self.get_color_rgba(self._bcolor_list)
    
    def get_bcolor_label(self):
        return self.get_color_rgba(self._bcolor_lable)

    def get_bcolor_tline(self):
        return self.get_color_rgba(self._bcolor_tline)

    def get_bcolor_graph(self):
        return self.get_color_rgba(self._bcolor_graph)

    def get_fcolor_button(self):
        return self._fcolor_button

    def get_bcolor_button(self):
        return self.get_color_rgba(self._bcolor_button)

    '''
    应用窗口属性
    '''
    def get_wsize(self):
        return self._wsize
    
    def get_wsize_w(self):
        return self._wsize['Width']

    def get_wsize_h(self):
        return self._wsize['Height']
    
    def set_wsize(self, width, height):
        self._wsize.update(Width = width, Height = height)

