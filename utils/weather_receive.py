def Receive(q, cap):
    if not cap.isOpened():
        print("Error opening video stream or file")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame from stream")
            break
        q.put(frame)
        print('receive')