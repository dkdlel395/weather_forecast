from PyQt5 import QtWidgets
import sys
from ui.main import Ui_MainWindow

def update_ui(rtsp_queue, pred_queue, yolo_queue, detect_queue):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, rtsp_queue, pred_queue, yolo_queue, detect_queue)
    MainWindow.show()
    sys.exit(app.exec_())