'''
OPENGL 显示中文
'''

from OpenGL.GL import *

import numpy as np
import freetype

Left   =  0
Center =  1
Right  =  2

class graphFont(object):

    def __init__(self, ttf, size, vector, spc = 0):
        self.__face = freetype.Face(ttf)     # 字体设置
        self.__size = size                   # 字体尺寸
        self.__vector = vector               # 矢量字体
        self.__spc = spc                     # 字符间距
        self.__init_asc()                    # ASCII文本提前生成，提高效率

    #------------------------------------------------------------------------------public--#
    # 设置字符间距
    def setSpace(self, spc):
        self.__spc = spc

    # 绘制文本
    def string(self, text, text_color, sep = None):
        if not isinstance(text, unicode) : text = text.decode('utf-8')

        self.__face.set_char_size(self.__size * 64, self.__size * 64, 96, 96)
        self.__face.set_pixel_sizes(self.__size, self.__size)

        metrics = self.__face.size
        ascender = metrics.ascender / 64.0

        # 获取一维字符图像
        width = int(self.__size * len(text) * 4)
        height = int(self.__size * 4)
        img = np.zeros([height, width])
        img = self.__fontString(img, 0, int(ascender), text, text_color, sep)
        
        # 获取三位字符图像
        height = img.shape[0]
        width = img.shape[1]

        imf = np.zeros([height, width, 4], np.uint8)
        for i in range(height):
            for j in range(width):
                imf[i, j, 0] = text_color[2]
                imf[i, j, 1] = text_color[1]
                imf[i, j, 2] = text_color[0]
                imf[i, j, 3] = img[i, j]
        return imf

    # 绘制数字
    def number(self, text, text_color):
        height = self._ascimg.shape[0]
        width = 0
        for sym in text:
            for i in range(1, len(self._asc)):
                if sym == self._asc[i]:
                    width += self._ascsep[i] - self._ascsep[i - 1]
        img = np.zeros([height, width, 4], np.uint8)
        width = 0
        for sym in text:
            for index in range(1, len(self._asc)):
                if sym == self._asc[index]:
                    for i in range(self._ascsep[index] - self._ascsep[index - 1]):
                        for h in range(height):
                            img[h][width + i][0] = text_color[2]
                            img[h][width + i][1] = text_color[1]
                            img[h][width + i][2] = text_color[0]
                            if self._ascimg[h][self._ascsep[index - 1] + i][3] != 0:
                                img[h][width + i][3] = text_color[3]
                            else:
                                img[h][width + i][3] = 0
                    width += self._ascsep[index] - self._ascsep[index - 1]
        return img
    
    # 获取字符纹理
    def getTexture(self, font):
        tid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tid)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, font.shape[1], font.shape[0], 0, GL_BGRA, GL_UNSIGNED_BYTE, font)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST) 
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        return tid

    # 绘制纹理 等比绘制
    def drawTexture(self, tid, px, py, fw, fh, frect):
        pw = fw / frect.w
        ph = fh / frect.h
        glBindTexture(GL_TEXTURE_2D, tid)
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(px, py)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(px, py + ph)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(px + pw, py + ph)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(px + pw, py)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    # 贴图绘制
    def draw(self, font, px, py, fw, fh):
        glRasterPos2d(px, py)
        glDrawPixels(fw, fh, GL_BGRA, GL_UNSIGNED_BYTE, font)      # 贴图

    # 精准位置 防止字体变形
    def prec(self, value):
        return int(value * 10000 + 5) / 10000.00

    #------------------------------------------------------------------------------private--#
    # 生成点阵字库
    def __init_asc(self):
        self._asc = '#1#234567890.#-#%# **'
        self._ascsep = []
        self._ascimg = self.string(self._asc, (255, 255, 255, 255), self._ascsep)

    # 拼接单个字符为字符串
    def __fontString(self, img, x_pos, y_pos, text, color, sep = None):
        prev_char = 0
        pen = freetype.Vector()
        pen.x = x_pos << 6
        pen.y = y_pos << 6

        cur_pen = freetype.Vector()
        pen_translate = freetype.Vector()

        for cur_char in text:

            # 获取文本图像 
            if self.__vector == True :
                self.__face.load_char(cur_char, 6)                   
            else :
                self.__face.load_char(cur_char, freetype.FT_LOAD_MONOCHROME | freetype.FT_LOAD_TARGET_MONO | freetype.FT_LOAD_RENDER)    

            kerning = self.__face.get_kerning(prev_char, cur_char)
            slot = self.__face.glyph                                 

            cur_pen.x = pen.x + kerning.x + self.__spc * 64          # 调整字符间距
            cur_pen.y = pen.y - slot.bitmap_top * 64

            self.__fontImage(img, slot.bitmap, cur_pen, color, sep)

            pen.x = cur_pen.x + slot.advance.x
            prev_char = cur_char
        
        width, height = self.__font_crop(img)

        # 图像裁剪和反转
        reimage = np.zeros([height, width], np.uint8)
        for h in range(height):
            for w in range(width):
                reimage[h, w] = img[height - h, w]

        return reimage

    # 边缘裁剪
    def __font_crop(self, img):
        height = img.shape[0]
        width = img.shape[1]

        left = 0
        right = 0
        top = 0
        bottom = 0

        # Left 精准检测
        for w in range(0, width):
            bflag = False
            for h in range(0, height):
                if img[h, w] != 0:
                    left = w
                    bflag = True
                    break
            if bflag == True:
                break

        # TOP 精准检测
        for h in range(0, height):
            bflag = False
            for w in range(0, width):
                if img[h, w] != 0:
                    top = h
                    bflag = True
                    break
            if bflag == True:
                break

        # right精准检测
        for w in reversed(range(width)):
            bflag = False
            for h in reversed(range(height)):
                if img[h, w] != 0:
                    right = w + left
                    bflag = True
                    break
            if bflag == True:
                break

        # bottom 精准检测
        for h in reversed(range(height)):
            bflag = False
            for w in reversed(range(width)):
                if img[h, w] != 0:
                    bottom = h + top
                    bflag = True
                    break
            if bflag == True:
                break

        # 此处为了防止半透明裁剪 所以上下左右分别扩展 Top Left
        return right, bottom

    # 字符串拼接
    def __fontImage(self, img, bitmap, pen, color, sep = None):

        x_pos = pen.x >> 6
        y_pos = pen.y >> 6

        cols = bitmap.width
        rows = bitmap.rows
        pitch = bitmap.pitch

        if sep is not None:
            sep.append(x_pos + cols)

        for row in range(rows):
            for col in range(cols):
                
                if self.__vector == True :
                    img[y_pos + row][col] = bitmap.buffer[row * cols + col]
                else :
                    inx = row * pitch + int(col / 8)
                    if (bitmap.buffer[inx] & 0x80 >> (col % 8)) == 0 :
                        img[y_pos + row][x_pos + col] = 0
                    else :
                        img[y_pos + row][x_pos + col] = color[3]

