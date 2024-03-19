from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import json

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.img_layout_widget = QtWidgets.QWidget(self.centralwidget)
        self.img_layout_widget.setGeometry(QtCore.QRect(50, 100, 1080, 600))
        self.img_layout_widget.setObjectName("img_layout_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.img_layout_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.img_layout_widget)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(1300, 410, 160, 80))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.take_roi_button = QtWidgets.QPushButton(self.centralwidget)
        self.take_roi_button.setGeometry(QtCore.QRect(1300, 300, 158, 91))
        self.take_roi_button.setObjectName("take_roi_button")

        self.take_roi_button2 = QtWidgets.QPushButton(self.centralwidget)
        self.take_roi_button2.setGeometry(QtCore.QRect(1300, 450, 158, 91))
        self.take_roi_button2.setObjectName("take_roi_button")

        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(1300, 150, 58, 131))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.pen_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pen_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("car/ui/pen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pen_button.setIcon(icon)
        self.pen_button.setObjectName("pen_button")
        self.verticalLayout_3.addWidget(self.pen_button)
        self.eraser_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.eraser_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("car/ui/eraser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.eraser_button.setIcon(icon1)
        self.eraser_button.setObjectName("eraser_button")
        self.verticalLayout_3.addWidget(self.eraser_button)

        self.point_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.point_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("car/ui/point.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.point_button.setIcon(icon2)
        self.point_button.setObjectName("point_button")
        self.verticalLayout_3.addWidget(self.point_button)

        self.reset_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.reset_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("car/ui/reset.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_button.setIcon(icon2)
        self.reset_button.setObjectName("reset_button")
        self.verticalLayout_3.addWidget(self.reset_button)

        self.befor_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.befor_data_button.setGeometry(QtCore.QRect(1300, 80, 151, 51))
        self.befor_data_button.setObjectName("befor_data_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actioncar_ROI = QtWidgets.QAction(MainWindow)
        self.actioncar_ROI.setObjectName("actioncar_ROI")
        # self.menu.addAction(self.actioncar_ROI)
        # self.menubar.addAction(self.menu.menuAction())

        ####
        self.roi_target_xy = [[(242,248),(250,259)],[(459,503),(459,558)]]
        self.roi_point_xy = []
        self.dragged_index = None
        self.img_layout_widget.mousePressEvent = self.mousePressEventHandler
        self.img_layout_widget.mouseMoveEvent = self.mouseMoveEvent
        self.img_layout_widget.mouseReleaseEvent = self.mouseReleaseEvent
        self.mode = 'default_mode'
        self.point_button.clicked.connect(self.point_button_click)
        self.eraser_button.clicked.connect(self.eraser_button_click)
        self.befor_data_button.clicked.connect(self.before_data_click)
        self.pen_button.clicked.connect(self.pen_button_click)
        self.take_roi_button.clicked.connect(self.take_roi_click)
        self.take_roi_button2.clicked.connect(self.take_roi_and_close)
        self.reset_button.clicked.connect(self.reset_button_click)
        ####

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.take_roi_button.setText(_translate("MainWindow", "ROI 확인하기"))
        self.take_roi_button2.setText(_translate("MainWindow", "ROI 적용하기"))
        self.label_2.setText(_translate("MainWindow", "도구"))
        self.befor_data_button.setText(_translate("MainWindow", "이전 기록 가져오기"))
        self.actioncar_ROI.setText(_translate("MainWindow", "car ROI"))


        # 카메라 연결
        self.rtsp_url = "rtsp://root:root@192.168.0.190:554/cam0_0"
        self.cap = cv2.VideoCapture(self.rtsp_url)
        self.setupTimer()

    def setupTimer(self):
        if hasattr(self, 'timer'):  # timer 속성이 이미 존재하는지 확인
            self.timer.timeout.disconnect()  # 기존 연결 해제
        self.timer = QTimer(self.MainWindow)
        if self.mode == 'default_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.update_frame)
        elif self.mode == 'take_roi_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.make_roi)
        elif self.mode == 'point_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.roi_make_frame)
        elif self.mode == 'eraser_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.roi_make_frame)
        elif self.mode == 'pen_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.roi_make_frame)
        elif self.mode == 'reset_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.roi_make_frame)
        elif self.mode == 'before_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.roi_make_frame)
        else:
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.roi_make_frame)
        self.timer.start(10)

    def make_roi(self):
        ret, frame = self.cap.read()
        if ret:
            if self.roi_point_xy:
                
                height, width, channels = frame.shape
                bytes_per_line = channels * width
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                mask = np.zeros(frame.shape, np.uint8)
                mask = cv2.polylines(mask, [np.array(self.roi_point_xy)], True, (255, 255, 255), 2)
                mask = cv2.fillPoly(mask.copy(), [np.array(self.roi_point_xy)], (255, 255, 255))


                roi_points = np.array(self.roi_point_xy, dtype=np.float32)
                targets = self.roi_target_xy
                for idx, (start_point, end_point) in enumerate(targets):
                    # 타겟이 ROI 내부에 있는지 확인
                    start_in_roi = cv2.pointPolygonTest(roi_points, start_point, False) >= 0
                    end_in_roi = cv2.pointPolygonTest(roi_points, end_point, False) >= 0

                    print(start_point, end_point)

                    if start_in_roi and end_in_roi:
                        print(f"타겟 {idx+1}번 ROI 안에 있습니다.")
                    else:
                        print(f"타겟 {idx+1}번 ROI 밖에 있습니다.")

                mask_frame = cv2.bitwise_and(mask, frame)
                convert_to_qt_format = QImage(mask_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(convert_to_qt_format)
                self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))
            else:
                print('좌표를 선택해')    



    def take_roi_and_close(self):
        with open('car/output/points.json', 'w') as json_file:
            json.dump(self.roi_point_xy, json_file)        
        self.cap.release()
        self.MainWindow.close()
        # QtWidgets.QApplication.quit()
        

    # self.roi_point_xy 최근접 이웃으로 재정비
    def reorder_roi_points(self):
        start_point = self.roi_point_xy[0]
        ordered_points = [start_point]
        remaining_points = self.roi_point_xy[1:]
        while remaining_points:
            last_point = ordered_points[-1]
            nearest_point = min(remaining_points, key=lambda p, last_point=last_point: (p[0] - last_point[0]) ** 2 + (p[1] - last_point[1]) ** 2)
            ordered_points.append(nearest_point)
            remaining_points.remove(nearest_point)
        self.roi_point_xy = ordered_points

    def roi_make_frame(self):
        ret, frame = self.cap.read()
        if ret:
            height, width, channels = frame.shape
            bytes_per_line = channels * width
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            for i in range(len(self.roi_point_xy)):
                cv2.circle(img=frame, center=self.roi_point_xy[i], radius=10, color=(255, 255, 0), thickness=2)
                if i > 0:
                    cv2.line(img=frame, pt1=self.roi_point_xy[i-1], pt2=self.roi_point_xy[i], color=(255, 0, 0), thickness=2)
            for lines in self.roi_target_xy:
                cv2.line(frame, lines[0],lines[1], (0,0,255),2)
            convert_to_qt_format = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

    def mousePressEventHandler(self, event):
        if self.mode == 'pen_mode':
            if event.button() == Qt.LeftButton:
                x = event.pos().x()
                print(x)
                y = event.pos().y()
                print(y)
                self.roi_point_xy.append([int((x*1920)/1080),int((y*1080)/600)])
                print("Mouse clicked at ({}, {}) inside img_layout_widget".format(x, y))
        elif self.mode == 'eraser_mode':
            if event.button() == Qt.LeftButton:
                x = event.pos().x()
                y = event.pos().y()
                x = max(0, min(x, 1080))
                x = int((x * 1920) / 1080)
                y = max(0, min(y, 600))
                y = int((y * 1080) / 600)

                for i in range(len(self.roi_point_xy)):
                    px, py = self.roi_point_xy[i]
                    if abs(px - x) <= 20 and abs(py - y) <= 20:
                        del self.roi_point_xy[i]
                        break
                print("Mouse clicked at ({}, {}) inside img_layout_widget".format(x, y))
        elif self.mode == 'point_mode' and event.buttons() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            x = max(0, min(x, 1080))
            x = int((x * 1920) / 1080)
            y = max(0, min(y, 600))
            y = int((y * 1080) / 600)
            for i in range(len(self.roi_point_xy)):
                px, py = self.roi_point_xy[i]
                if abs(px - x) <= 20 and abs(py - y) <= 20:
                    self.dragged_index = i  # 드래그된 객체의 인덱스를 저장합니다.
                    self.drag_offset = (x - px, y - py)  # 마우스와 객체 사이의 오프셋을 계산합니다.
                    break
        elif self.mode == 'reset_mode':
            self.rot_point_xy = []
        else: pass

    def mouseMoveEvent(self, event):
        if self.mode == 'point_mode' and event.buttons() == Qt.LeftButton:
            if self.dragged_index is not None:  # 드래그 중인 객체가 있을 때만 실행합니다.
                x = event.pos().x()
                y = event.pos().y()
                x = max(0, min(x, 1080))
                x = int((x * 1920) / 1080)
                y = max(0, min(y, 600))
                y = int((y * 1080) / 600)
                
                px, py = self.roi_point_xy[self.dragged_index]
                dx, dy = self.drag_offset
                self.roi_point_xy[self.dragged_index] = [x - dx, y - dy]
        else: pass

    def mouseReleaseEvent(self, event):
        print('최종 좌표 : ',self.dragged_index)
        if self.mode == 'point_mode' and event.button() == Qt.LeftButton:
            self.dragged_index = None  # 드래그를 뗀 후에는 인덱스를 초기화합니다.
        else: pass

    def closeEvent(self, event):
        self.cap.release()

    def point_button_click(self):
        self.mode = 'point_mode'
        print(self.mode)
        self.setupTimer()

    def eraser_button_click(self):
        self.mode = 'eraser_mode'
        print(self.mode)
        self.setupTimer()

    def before_data_click(self):
        self.mode = 'before_mode'
        with open('car/output/points.json','r') as f:
            self.roi_point_xy = json.load(f)
        print(self.mode)
        self.setupTimer()

    def take_roi_click(self):
        self.mode = 'take_roi_mode'
        print(self.mode)
        self.setupTimer()
    
    def pen_button_click(self):
        self.mode = 'pen_mode'
        print(self.mode)
        self.setupTimer()
    
    def reset_button_click(self):
        self.mode = 'reset_mode'
        print(self.mode)
        self.roi_point_xy = []
        self.setupTimer()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
