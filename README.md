### 요구사항

<table>
  <tr>
    <th>요구사항</th>
    <th>버전 v_0.1</th>
    <th>버전 v_0.0</th>
  </tr>
  <tr>
    <td>차량 및 보행자 탐지 (사전 훈련된 모델)</td>
    <td>✔️</td>
    <td></td>
  </tr>
  <tr>
    <td>PyQT5 기반 GUI</td>
    <td>✔️</td>
    <td></td>
  </tr>
  <tr>
    <td>차량 차선 이탈 탐지</td>
    <td>✔️</td>
    <td></td>
  </tr>
  <tr>
    <td>ROI 사용자 정의 기능</td>
    <td>✔️</td>
    <td></td>
  </tr>
  <tr>
    <td>비동기 처리 UI, 날씨, 모델, 차량 탐지</td>
    <td>✔️</td>
    <td></td>
  </tr>
  <tr>
    <td>실시간 처리 최적화 프로그램</td>
    <td>✔️</td>
    <td></td>
  </tr>
  <tr>
    <td>날씨, 차량 이상 탐지 로그 및 알림</td>
    <td>✔️</td>
    <td></td>
  </tr>
  <tr>
    <td>GPU 서버 학습</td>
    <td></td>
    <td>✔️</td>
  </tr>
  <tr>
    <td>날씨 예측 모델</td>
    <td></td>
    <td>✔️</td>
  </tr>
</table>


-------------------

1. 학습 준비
    - EDA 2024년 2월 16일
        - 종류 : 차량번호판인식 (1,007,219장) , 차종외관 인식 (1,001,657장)
            - 차량번호판 인식
            - 날씨 : 맑음 839,597 (83.8%), 강우 152,988 (15.3%) , 안개 9,072 (0.9%)
            - 시간 : 심야 32.713 (3.3%), 오전 406.966 (40.6%), 오후 408,439 (40.8%), 저녁 153,539 (15.3%)
            - 차종외관인식
                - 날씨 : 맑음 855.602(84.9%)장, 강우 142,495장(14.1%), 안개 9,122장(0.9%)
                - 시간 : 심야 36,144 (3.6%), 오전 401,501 (39.9%), 오후 404,044 (40.1%), 저녁 165,530 (16.4%)
            - 데이터 스케일링
                - 분포가 많은 데이터 : sunny, morning, afternoon → 줄이기
                - 분포가 적은 데이터 : rain, fog, dawn → 늘리기
        - train : image
            - 계절(season) 데이터를 추가하려했으나 여름,가을만 존재하여 제외
        - label : weather (+time(extract_time,date))
        - resolution : UHD, FHD 두가지 사진 비율로 통합 필요

    - 필요 데이터
        - Raw_Data_Info : weather(날씨), resolution(해상도)
        - Source_Data_Info : extract_time(사진 촬영 시간)
        - Learning_Data_Info : path(파일경로), json_data_id(파일이름)
    - 데이터 수집 2024년 2월 21일
        - AI-HUB CCTV 기반 차량정보 데이터
    - 데이터 엔지니어링
        - JSON 에서 필요 데이터만 추출
        - image resize : FHD, UHD to (640 x 480)
    - 학습 환경 구축
        - PC : GPU server, NAS 사용
        - NAS : 데이터 저장소
        - GPU Server : NAS 데이터로 모델 학습
    - 학습 모델 선택
        - CNN RESNET
    - 검증 방법
        - F1 score, Acc

2. 학습 진행
    - 학습 모델
        - CNN RESNET, multi classfication
    - 검증 방법
        - F1 score, Acc
    - 결과
        - 정확도 : 85%
        - 학습 시간 : 69h
    - 피드백
        - 예측이 어려운 상황이 많음
            - 비가 내리고 있으나 바닥이 말라있을때, 비가 그쳤으나 바닥에 물이 고여있을때
            - 그늘에서의 예측 확률 저하
            - cctv 특성상 500m 정도의 먼거리의 object detection의 어려움