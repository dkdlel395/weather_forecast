from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from ultralytics import YOLO
import threading
import numpy as np
import queue
import sys
import cv2
import json
import time
import roi
import datetime
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Dict

class Ui_MainWindow(object):
    def setupUi(self, MainWindow,rtsp_q, pred_q, yolo_q):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50 ,100, 1080, 600))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1300, 150, 65, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1300, 250, 65, 17))
        self.label_3.setObjectName("label_3")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(1300, 670, 131, 61))
        self.checkBox.setObjectName("checkBox")

        self.verticalLayout.addWidget(self.label)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(1300, 800, 160, 80))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.take_roi_button = QtWidgets.QPushButton(self.centralwidget)
        self.take_roi_button.setGeometry(QtCore.QRect(1300, 800, 158, 91))
        self.take_roi_button.setObjectName("take_roi_button")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1116, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actioncar_ROI = QtWidgets.QAction(MainWindow)
        self.actioncar_ROI.setObjectName("actioncar_ROI")
        self.menu.addAction(self.actioncar_ROI)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ####
        self.rtsp_q = rtsp_q
        self.yolo_q = yolo_q
        # self.model = YOLO('C:/Users/jhp12/Desktop/park/git/weather-forecast/car/yolov8m.pt')
        self.actioncar_ROI.triggered.connect(self.open_roi_ui)
        self.checkBox.stateChanged.connect(self.checkbox_cilck)
        self.take_roi_button.clicked.connect(self.take_roi_click)
        self.mode = 'default_mode'
        # self.rtsp_url = "rtsp://root:root@192.168.0.190:554/cam0_0"
        # print('셋업')
        self.json_check()
        self.roi_target_xy = [[(242,248),(250,259)],[(459,503),(459,558)]]
        ####

        self.setupTimer()

    def setupTimer(self):
        if hasattr(self, 'timer'):
            self.timer.timeout.disconnect()
        self.timer = QTimer(self.MainWindow)

        if self.mode == 'check_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.roi_check)
        elif self.mode == 'default_mode':
            print('Timer : ',self.mode)
            self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "(카메라 로딩 중)"))
        self.label_2.setText(_translate("MainWindow", "(차량 인식 중)"))
        self.label_3.setText(_translate("MainWindow", "(사람 인식 중)"))
        self.menu.setTitle(_translate("MainWindow", "설정"))
        self.take_roi_button.setText(_translate("MainWindow", "ROI 가져오기"))
        self.actioncar_ROI.setText(_translate("MainWindow", "car ROI"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))

    def open_roi_ui(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = roi.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def roi_check(self):
        while self.yolo_q.empty():
            time.sleep(0.01)
        
        data = self.yolo_q.get()
        frame = data['img']
        height, width, channels = frame.shape
        bytes_per_line = channels * width
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mask = np.zeros(frame.shape, np.uint8)
        mask = cv2.polylines(mask, [np.array(self.roi_point_xy)], True, (255, 255, 255), 2)
        mask = cv2.fillPoly(mask.copy(), [np.array(self.roi_point_xy)], (255, 255, 255))
        mask_frame = cv2.bitwise_and(mask, frame)
        convert_to_qt_format = QImage(mask_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(convert_to_qt_format)
        self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

        self.yolo_q.task_done()


    def take_roi_click(self):
        print('take roi click')
        with open('car/output/points.json') as f:
            self.roi_point_xy = json.load(f)
        print('현재 ROI : ', self.roi_point_xy)

    def json_check(self):
        with open('car/output/points.json') as f:
            self.roi_point_xy = json.load(f)
        print('현재 ROI : ', self.roi_point_xy)

    def update_frame(self):
        if self.yolo_q.empty():
            time.sleep(0.01)
        else:
            data = self.yolo_q.get()
            frame = data['img']
            car_cnt = data['car_cnt']
            human_cnt = data['human_cnt']
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w

            self.label_2.setText("차량수: {}대".format(car_cnt))
            self.label_3.setText("사람수: {}명".format(human_cnt))
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

            self.yolo_q.task_done()

    def checkbox_cilck(self):
        if self.checkBox.isChecked():
            self.mode = 'check_mode'
        else:
            self.mode = 'default_mode'
        self.setupTimer()



def receive(q,cap, cap_add):
    if not cap.isOpened():
        print("Error opening video stream or file")
        time.sleep(0.1)
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Queue에 쌓여있는 데이터 개수:", q.qsize())
            print("Error reading frame from stream")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q.put(frame)
        if q.qsize() >= 20:
            q.get()
            q.task_done()
            # time.sleep(0.1)


def json_check():
    global roi_point_xy
    with open('car/output/points.json') as f:
        roi_point_xy = json.load(f)
        f.close()

def prediction(rtsp_q,pred_q, model):
    while True:
        frame = rtsp_q.get()
        results = model.predict(frame, save=False, conf=0.4, verbose=False)# , imgsz=(640,640))
        rtsp_q.task_done()
        pred_q.put(results)


def processing(pred_q, yolo_q):
    while True:
        while pred_q.empty():

            time.sleep(0.25)
        results = pred_q.get()
        for result in results:
            boxes = result.boxes
            img = result.orig_img
            boxes_xy = boxes.xyxy
            clses = boxes.cls

            car_cnt   = 0
            human_cnt = 0
            target_xy = []
            for cls, box in zip(clses, boxes_xy):
                if cls == 0 or cls == 2:
                    if cls == 0:
                        human_cnt +=1
                    if cls in [2, 3, 5, 7]:
                        car_cnt +=1
                    x_min, y_min, x_max, y_max = box.tolist()

                    target_xy.append([(int(x_min),int(y_max)+1), (int(x_max),int(y_max)+1)])
                    # print(target_xy)
                    cv2.line(img, (int(x_min), int(y_max)), (int(x_max), int(y_max)), (0, 0, 255), 2)

                    roi_points = np.array(roi_point_xy, dtype=np.float32)
                    for idx, (start_point, end_point) in enumerate(target_xy):
                        # print(start_point, end_point)
                        start_in_roi = cv2.pointPolygonTest(roi_points, start_point, False) >= 0
                        end_in_roi = cv2.pointPolygonTest(roi_points, end_point, False) >= 0
                        if cls in [2, 3, 5, 7]:
                            if start_in_roi and end_in_roi:
                                print(f"CAR {idx+1}번 ROI 안에 있습니다.")
                                pass
                            else:
                                print(f"CAR {idx+1}번 ROI 밖에 있습니다.")
                                pass
                        if cls == 0:
                            if start_in_roi and end_in_roi:
                                print(f'Human {idx+1}번 ROI 안에 있습니다')
                            else:
                                print(f"CAR {idx+1}번 ROI 밖에 있습니다.")

        yolo_q.put({'img':img,'car_cnt':car_cnt,'human_cnt':human_cnt})
        pred_q.task_done()

def update_ui(rtsp_queue, pred_queue, yolo_queue):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, rtsp_queue, pred_queue, yolo_queue)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    model = YOLO('C:/Users/jhp12/Desktop/park/git/weather-forecast/car/yolov8x.pt')
    rtsp_url = "rtsp://root:root@192.168.0.190:554/cam0_0"
    cap = cv2.VideoCapture(rtsp_url)

    executor = ThreadPoolExecutor()

    # 큐 생성
    rtsp_queue = Queue()
    pred_queue = Queue()
    yolo_queue = Queue()

    # p1 = threading.Thread(target=receive, args=(rtsp_queue,cap))
    # p2 = threading.Thread(target=prediction, args=(rtsp_queue,pred_queue, model))
    # p3 = threading.Thread(target=processing, args=(pred_queue,yolo_queue))
    # p1.start()
    # p2.start()
    # p3.start()

    json_check()

    # 스레드 시작
    executor.submit(receive, rtsp_queue, cap, rtsp_url)
    executor.submit(prediction, rtsp_queue, pred_queue, model)
    executor.submit(processing, pred_queue, yolo_queue)
    # executor.submit(update_ui, rtsp_queue, pred_queue, yolo_queue)

    update_ui(rtsp_queue, pred_queue, yolo_queue)