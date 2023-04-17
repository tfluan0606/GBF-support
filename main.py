import cv2 as cv
import numpy as np
import pyautogui
from windowcapture import WindowCapture

wincap = WindowCapture('グランブルーファンタジー - Iron')

while True:
    screenshot = wincap.get_screenshot()
    cv.imshow('Test',screenshot)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done.')