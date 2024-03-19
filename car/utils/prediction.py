def prediction(rtsp_q,pred_q, model):
    while True:
        frame = rtsp_q.get()
        results = model.predict(frame, save=False, conf=0.5, verbose=False)
        rtsp_q.task_done()
        pred_q.put(results)