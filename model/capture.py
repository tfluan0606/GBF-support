import cv2 as cv
import numpy as np
from ctypes import windll
import win32gui
import win32ui
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
result_path = os.path.join(current_dir, 'questresult.jpg')
ready_path = os.path.join(current_dir, 'ready.jpg')

class Capture:

    # properties
    hwnd = None
    hwnd_dc = None
    mfc_dc = None 
    save_dc = None
    bitmap = None
    w = 0
    h = 0
    max_val = 0
    is_battling = 1

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        left, top, right, bottom = win32gui.GetClientRect(self.hwnd) 
        self.w = right - left
        self.h = bottom - top

    def get_frame(self):
        windll.user32.SetProcessDPIAware()
        self.hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        self.mfc_dc = win32ui.CreateDCFromHandle(self.hwnd_dc)
        self.save_dc = self.mfc_dc.CreateCompatibleDC()
        self.bitmap = win32ui.CreateBitmap()
        self.bitmap.CreateCompatibleBitmap(self.mfc_dc, self.w, self.h)
        self.save_dc.SelectObject(self.bitmap)
        
        result = windll.user32.PrintWindow(self.hwnd, self.save_dc.GetSafeHdc(), 3)

        bmpinfo = self.bitmap.GetInfo()
        bmpstr = self.bitmap.GetBitmapBits(True)

        _img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        _img = np.ascontiguousarray(_img)[..., :-1]  # make image C_CONTIGUOUS and drop alpha channel
        #im = Image.frombuffer("RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)
        #img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        #img = np.ascontiguousarray(img)[..., :-1]  # make image C_CONTIGUOUS and drop alpha channel
        img = _img.copy()

        self.rlease_mem()
        return img

    def rlease_mem(self):
        win32gui.DeleteObject(self.bitmap.GetHandle())
        self.save_dc.DeleteDC()
        self.mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwnd_dc)

    def match_frame(self):
        current_frame = self.get_frame()
        if self.is_battling:
            target_frame = cv.imread(result_path, cv.IMREAD_UNCHANGED)
            threshold = 0.8
        else:
            target_frame = cv.imread(ready_path, cv.IMREAD_UNCHANGED)
            threshold = 0.9
        match_result = cv.matchTemplate(current_frame, target_frame, cv.TM_CCOEFF_NORMED)
        min_val, self.max_val, min_loc, max_loc = cv.minMaxLoc(match_result)
        if self.max_val >= threshold:
            return 1
        return 0
