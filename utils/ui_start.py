import sys
from PyQt5 import QtWidgets
from ui.main_weather import Ui_MainWindow

def ui_start(data_q):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())