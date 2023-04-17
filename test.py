from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
import cv2
import numpy as np

def convertQImageToMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''
    # Format_RGB32 = 4,存入格式為B,G,R,A 對應 0,1,2,3
    # RGB32圖像每個像素用32比特位表示，占4個字節，
    # R，G，B分量分別用8個bit表示，存儲順序為B，G，R，最後8個字節保留
    incomingImage = incomingImage.convertToFormat(4)
    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
    # arr為BGRA，4通道圖片
    return arr


hwnd = win32gui.FindWindow(None, 'グランブルーファンタジー - Iron')
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()

while True:

    img = screen.grabWindow(hwnd).toImage()
    img=convertQImageToMat(img)#將獲取的圖像從QImage轉換為RBG格式
    cv2.imshow("asd",img)      #imshow
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
        