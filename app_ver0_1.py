from torchinfo import summary
import torch
import cv2
import threading
import queue
from utils.network import network

from utils.weather_receive import Receive
from utils.weather_predict import predict
from utils.ui_start import ui_start

class_num = 3
model = network(class_num)
# print("###모델 정의 완료(resnet18)###\n", summary(model))

# RTSP 주소
rtsp_url = "rtsp://root:root@192.168.0.190:554/cam0_0"
save_path = "Z:/DEV/weather-forcast/CCTV_DATA/data/gpu_test_v01.pt"
model.load_state_dict(torch.load(save_path, map_location=torch.device('cpu')))
model.eval()

q = queue.Queue()
data_q = queue.Queue()
cap = cv2.VideoCapture(rtsp_url)

p3 = threading.Thread(target=ui_start, args=(data_q))
p1 = threading.Thread(target=Receive, args=(q, cap))
p2 = threading.Thread(target=predict, args=(q, data_q, model))
p3.start()
p1.start()
p2.start()


p1.join()
p2.join()