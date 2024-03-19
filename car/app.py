from ultralytics import YOLO
import cv2
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from utils.receive import receive
from utils.json_check import json_check
from utils.prediction import prediction
from utils.update_ui import update_ui
from utils.processing import processing

model = YOLO('C:/Users/jhp12/Desktop/park/git/weather-forecast/car/yolov9e.pt')
rtsp_url = "rtsp://root:root@192.168.0.190:554/cam0_0"
# rtsp_url = "C:/Users/jhp12/Desktop/park/git/weather-forecast/car/ui/cctv_test_1.mp4"
cap = cv2.VideoCapture(rtsp_url)
rtsp_queue = Queue()
pred_queue = Queue()
yolo_queue = Queue()
detect_queue = Queue()
json_check()
executor = ThreadPoolExecutor()
executor.submit(receive, rtsp_queue, cap, rtsp_url)
executor.submit(prediction, rtsp_queue, pred_queue, model)
executor.submit(processing, pred_queue, yolo_queue, detect_queue)
update_ui(rtsp_queue, pred_queue, yolo_queue, detect_queue)