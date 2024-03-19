import time
import cv2
import numpy as np

def processing(pred_q, yolo_q,detect_q, roi_point_xy):
    while True:
        while pred_q.empty():
            # print('pred_q empty')
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
                    cv2.line(img, (int(x_min), int(y_max)), (int(x_max), int(y_max)), (0, 0, 255), 2)
                    roi_points = np.array(roi_point_xy, dtype=np.float32)
                    for idx, (start_point, end_point) in enumerate(target_xy):
                        start_in_roi = cv2.pointPolygonTest(roi_points, start_point, False) >= 0
                        end_in_roi = cv2.pointPolygonTest(roi_points, end_point, False) >= 0
                        # print('감지한 cls : ', cls)
                        if cls in [2, 3, 5, 7]:
                            if start_in_roi and end_in_roi:
                                # print(f"CAR {idx+1}번 ROI 안에 있습니다.")
                                pass
                            else:
                                # print(f"CAR {idx+1}번 ROI 밖에 있습니다.")
                                detect_q.put({'img':img[int(y_min):int(y_max), int(x_min):int(x_max)], 'type':'car'})
                                pass
                        if cls == 0:
                            if start_in_roi and end_in_roi:
                                # print(f'Human {idx+1}번 ROI 안에 있습니다')
                                detect_q.put({'img':img[int(y_min):int(y_max), int(x_min):int(x_max)], 'type':'human'})
                            else:
                                # print(f"Human {idx+1}번 ROI 밖에 있습니다.")
                                pass
        yolo_q.put({'img':img,'car_cnt':car_cnt,'human_cnt':human_cnt})
        pred_q.task_done()
        if yolo_q.qsize() >= 20:
            yolo_q.get()
            yolo_q.task_done()