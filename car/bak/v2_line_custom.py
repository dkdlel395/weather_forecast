import cv2 as cv
import cv2
import numpy as np
import json

img_size = [640,480]
window_padding = 100
pts = []
resultforJSON = []
file_path = 'car/output/sample.json'


def draw_roi(event, x, y, flags, param):
    # roi 검출을 위한 함수 정의

    img2 = img.copy()

    # 마우스 왼쪽버튼을 클릭하면
    if event == cv.EVENT_LBUTTONUP:
        if x < 0 or x >= img.shape[1] or y < 0 or y >= img.shape[0]:
            # 근처 최대값 좌표로 변경
            x = max(0, min(x, img.shape[1] - 1))
            y = max(0, min(y, img.shape[0] - 1))
        pts.append((x, y))

        # 정상적으로 추가되는지 출력으로 확인
        print('포인트 #%d 좌표값(%d,%d)' % (len(pts), x, y))

        # 포인트 순서와 좌표값을 딕셔너리 형태로 추가해준다
        resultforJSON.append({'point': [len(pts)],
                              'coordinate': [[int(x), int(y)]]})

    # 마우스 오른쪽버튼을 클릭하면
    if event == cv.EVENT_RBUTTONDOWN:
        # 클릭했던 포인트를 삭제한다
        pts.pop()

    # 마우스 중앙(휠)버튼을 클릭하면
    if event == cv.EVENT_MBUTTONDOWN:
        # 총 포인트 개수 출력
        print('총 %d개의 포인트 설정' % len(pts))

        # 컬러를 다루기 때문에 np로 형변환
        mask = np.zeros(img.shape, np.uint8)

        # pts 2차원을 이미지와 동일하게 3차원으로 재배열
        points = np.array(pts, np.int32)
        points = points.reshape((-1, 1, 2))

        # 포인트와 포인트를 연결하는 라인을 설정
        mask = cv.polylines(mask, [points], True, (255, 255, 255), 2)

        # 폴리곤 내부 색상 설정
        mask2 = cv.fillPoly(mask.copy(), [points], (255, 255, 255))

        # mask와 mask2에 중첩된 부분을 추출
        ROI = cv.bitwise_and(mask2, img)

        # resultforJSON에 저장된 내용을 json파일로 추출
        with open(file_path, 'w') as outfile:
            json.dump(resultforJSON, outfile, indent=4)

        # ROI 이미지 저장
        cv.imwrite('car/output/ROI.png', ROI)

        # ROI 이미지 출력
        cv.imshow('ROI', ROI)
        cv.waitKey(0)

    # 포인트를 '원'으로 표시
    if len(pts) > 0:
        cv.circle(img2, pts[-1], 3, (0, 0, 255), -1)

    # 포인트를 연결하는 선 표시
    if len(pts) > 1:
        for i in range(len(pts) - 1):
            cv.circle(img=img2, center=pts[i], radius=3, color=(255, 0, 0), thickness=2)
            cv.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

    # 이미지 출력
    # cv2.resizeWindow(winname='image', width=img_size[0]+window_padding, height=img_size[1]+window_padding)
    cv.imshow('image', img2)


# 이미지 불러오기 및 크기 조절
img = cv.imread('image/image.jpg')
img = cv2.resize(img, dsize=(img_size[0], img_size[1]), interpolation=cv2.INTER_CUBIC)

# 윈도우 생성 및 마우스 콜백 함수 설정
cv.namedWindow('image')
cv.setMouseCallback('image', draw_roi)

while True:
    # 'q' 키를 누르면 종료
    if cv.waitKey(1) & 0xFF == 27:
        break

    # 's' 키를 누르면 현재 설정 저장
    if cv.waitKey(1) & 0xFF == ord('s'):
        saved_data = {'ROI': pts}

    # 루프 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()