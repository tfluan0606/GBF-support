from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from view.initial_window import Ui_initial_window
from view.function_window import Ui_function_window
from model.capture import Capture 
from model.notifier import notify
import sys, threading , pyautogui, time


class main_window(QMainWindow):

    window_name = None
    is_capture = 0

    def __init__(self):
        super(main_window,self).__init__()
        self.start_initial_window()

    #initial window
    def start_initial_window(self):
        if self.is_capture:
            self.is_capture = 0
        self.ui = Ui_initial_window()
        self.ui.setupUi(self)
        self.refresh_list() #init combox box item
        self.initial_button_linking() #init button event
        self.setWindowTitle('FA通知小精靈')
        self.setWindowIcon(QIcon('model/favicon.ico'))

    #link initial window button
    def initial_button_linking(self):
        self.ui.refresh.clicked.connect(self.refresh_list) #refresh button connect event
        self.ui.start.clicked.connect(self.start_function_window) #summit window hwnd then switch to function window

    #function window
    #after clicking starting, cv listen game window
    def start_function_window(self):
        self.window_name = self.ui.windowlist.currentText()
        #cv start
        self.is_capture = 1
        working = threading.Thread(target=self.start_capturing)
        working.start()
        #print(self.window_name)
        self.ui = Ui_function_window()
        self.ui.setupUi(self)
        self.setWindowTitle('FA通知小精靈')
        self.function_button_linking()

    #link function window button
    def function_button_linking(self):
        self.ui.recreate.clicked.connect(self.start_initial_window)

    #refresh window list
    def refresh_list(self):
        self.ui.windowlist.clear()
        for x in pyautogui.getAllWindows():
            if(x.title != ''):
                self.ui.windowlist.addItem(x.title)

    #opencv part
    def start_capturing(self):
        capture = Capture(self.window_name)
        #count = 0
        #while count != 50:
        while self.is_capture:
            if capture.match_frame():
                if capture.is_battling:
                    notify()
                    capture.is_battling = 0
                else:
                    #find ready pic, battle start
                    capture.is_battling = 1
            time.sleep(0.2)
    
    def closeEvent(self, event):
        win.is_capture = 0

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = main_window()
    win.show()
    sys.exit(app.exec_())
    