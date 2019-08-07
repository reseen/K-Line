
import numpy as np

class point():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        str = 'x = %d y = %d' % (self.x, self.y)
        return str

class rect():
    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def __str__(self):
        str = 'x = %d y = %d w = %d h = %d' % (self.x, self.y, self.w, self.h)
        return str

class rectEx():
    def __init__(self, x = 0.0, y = 0.0, width = 0.0, height = 0.0, frect = None):
        if frect != None:
            self.set_rectex(x, y, width, height, frect)
        else:
            pass

    def set_rectex(self, x, y, width, height, frect):
        if (x > 1.0):
            self.x = x
            self.perc_x = x / frect.w
        else:
            self.x = x * float(frect.w)
            self.perc_x = x

        if (y > 1.0):
            self.y = y
            self.perc_y = y / float(frect.h)
        else:
            self.y = y * float(frect.h)
            self.perc_y = y

        if (width > 1.0):
            self.w = width
            self.perc_w = width / float(frect.w)
        else:
            self.w = width * float(frect.w)
            self.perc_w = width
            
        if (height > 1.0):
            self.h = height
            self.perc_h = height / float(frect.h)
        else:
            self.h = height * float(frect.h)
            self.perc_h = height

    def __str__(self):
        str = 'x = %d perc_x = %f\r\ny = %d perc_y = %f\r\nw = %d perc_w = %f\r\nh = %d perc_h = %f' \
            % (self.x, self.perc_x, self.y, self.perc_y, self.w, self.perc_w, self.h, self.perc_h)
        return str
        