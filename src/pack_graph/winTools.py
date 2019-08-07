import ctypes
import win32con
import win32gui

class winTools(object):

    def __init__(self, name):
        self._name = name

    def set_appID(self):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self._name)

    def set_icon(self, icon_path):
        icon = win32gui.LoadImage(0, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_DEFAULTSIZE | win32con.LR_LOADFROMFILE)
        handle = win32gui.FindWindow(None, self._name) 
        win32gui.SendMessage(handle, win32con.WM_SETICON, win32con.ICON_BIG, icon)
        win32gui.SendMessage(handle, win32con.WM_SETICON, win32con.ICON_SMALL, icon)

    def destroy_icon(self, icon):
        win32gui.DestroyIcon(icon)