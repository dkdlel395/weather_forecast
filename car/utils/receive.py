import cv2
def receive(q,cap, cap_add):
    if not cap.isOpened():
        print("Error opening video stream or file")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Queue에 쌓여있는 데이터 개수:", q.qsize())
            print("erro : RTSP 에러")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q.put(frame)
        if q.qsize() >= 20:
            q.get()
            q.task_done()