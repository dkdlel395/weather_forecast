from utils.dataset import dataset
from torch.utils.data import DataLoader
import time
import torch
import cv2

def predict(q, data_q, model):
    print('predict')
    while True:
        while q.empty():
            print('wait')
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
        # return frame, predicted_weather
                # uiopen(frame, predicted_weather)
        data_q.put((frame,predicted_weather))
        q.task_done()
        # cv2.putText(frame, predicted_weather, (1900 - 180, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # cv2.imshow("IP Camera Stream", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        