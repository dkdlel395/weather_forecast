import torch
import torch.nn as nn
from torchvision import models
from torchinfo import summary
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import ToTensor, Resize
import cv2
import threading
import queue
import time

class network(nn.Module):
    def __init__(self, class_num):
        super().__init__()
        self.class_num = class_num
        self.init = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=(1, 1))
        self.model = models.resnet18(pretrained=True)
        self.gradlayer = self.model.layer4[-1]
        self.num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(self.num_ftrs, class_num)

    def forward(self, x):
        output = self.init(x)
        output = self.model(output)
        return output

class dataset(Dataset):
    def __init__(self, frame):
        self.frame = frame

    def __len__(self):
        return 1  # Continuous stream, so length is 1

    def __getitem__(self, index):
        frame = self.frame

        # Resize to a fixed size for the model (adjust dimensions if needed)
        resized_frame = cv2.resize(frame, (640, 480))

        # Convert to PyTorch tensor and normalize (adjust normalization if needed)
        frame_tensor = ToTensor()(resized_frame)
        frame_tensor = frame_tensor.float()
        # Normalize (example): frame_tensor = (frame_tensor - 0.5) / 0.5

        return frame_tensor

class_num = 3
model = network(class_num)
print("###모델 정의 완료(resnet18)###\n", summary(model))

# RTSP 주소
rtsp_url = "rtsp://root:root@192.168.0.190:554/cam0_0"
save_path = "Z:/DEV/weather-forcast/CCTV_DATA/data/gpu_test_v01.pt"
model.load_state_dict(torch.load(save_path, map_location=torch.device('cpu')))
model.eval()

q=queue.Queue()
cap = cv2.VideoCapture(rtsp_url)

def Receive():
    if not cap.isOpened():
        print("Error opening video stream or file")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame from stream")
            break
        q.put(frame)

def Display():
    while True:
        while q.empty():
            time.sleep(0.01)
        frame = q.get()
        test_dataset = dataset(frame)
        test_dataloader = DataLoader(test_dataset, batch_size=1)
        for inputs in test_dataloader:
            with torch.no_grad():
                outputs = model(inputs).squeeze()
            _, predicted = torch.max(outputs, dim=0)

            if predicted.item() == 0:
                predicted_weather = "fog"
            elif predicted.item() == 1:
                predicted_weather = "rain"
            elif predicted.item() == 2:
                predicted_weather = "sunny"

            print(f"예측 결과: {predicted_weather}")
        
        cv2.putText(frame, predicted_weather, (1900 - 180, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("IP Camera Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        q.task_done()

if __name__ == '__main__':
    p1 = threading.Thread(target=Receive)
    p2 = threading.Thread(target=Display)
    p1.start()
    p2.start()

    p1.join()  # Receive 스레드 종료 대기
    if cap is not None:  # cap 객체가 정상적으로 생성된 경우
        cap.release()
        cv2.destroyAllWindows()