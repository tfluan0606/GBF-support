from winotify import Notification
import os

def notify():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ico_path = os.path.join(current_dir, 'favicon.ico')

    toaster = Notification(app_id="gbf",title='FA通知',msg='FA完了！繼續按下一場！',icon=ico_path)
    toaster.show()