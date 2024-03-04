# **일정** (3월 4일)

1. 학습 준비
    - EDA 2024년 2월 16일
        - 종류 : 차량번호판인식 (1,007,219장) , 차종외관 인식 (1,001,657장)
            - 차량번호판 인식
            - 날씨 : 맑음 839,597 (83.8%), 강우 152,988 (15.3%) , 안개 9,072 (0.9%)
            - 시간 : 심야 32.713 (3.3%), 오전 406.966 (40.6%), 오후 408,439 (40.8%), 저녁 153,539 (15.3%)
            
            ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/d10e0519-c0eb-462b-9fce-35c5338cbc45/17a07987-fc71-460b-8ec2-e7df8c67061b/Untitled.png)
            
            - 차종외관인식
                - 날씨 : 맑음 855.602(84.9%)장, 강우 142,495장(14.1%), 안개 9,122장(0.9%)
                - 시간 : 심야 36,144 (3.6%), 오전 401,501 (39.9%), 오후 404,044 (40.1%), 저녁 165,530 (16.4%)
            - 데이터 스케일링
                - 분포가 많은 데이터 : sunny, morning, afternoon → 줄이기
                - 분포가 적은 데이터 : rain, fog, dawn → 늘리기
                - 
        - train : image
            - 계절(season) 데이터를 추가하려했으나 여름,가을만 존재하여 제외
        - label : weather (+time(extract_time,date))
        - resolution : UHD, FHD 두가지 사진 비율로 통합 필요
    
    - 데이터 구조
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/d10e0519-c0eb-462b-9fce-35c5338cbc45/597e5c1c-6e8f-4c20-a44b-0e87e0b2314b/Untitled.png)
        
    
    - 필요 데이터
        - Raw_Data_Info : weather(날씨), resolution(해상도)
        - Source_Data_Info : extract_time(사진 촬영 시간)
        - Learning_Data_Info : path(파일경로), json_data_id(파일이름)
    - 데이터 수집 2024년 2월 21일
        - [AI-HUB CCTV 기반 차량정보 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=71573)
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

1. 모델 학습 2024년 2월 27일 
    - 정확도 :
    - 학습 시간 :

1. 모델 서비스 2024년 3월 4일 
    - web ?
    - pyqt ?
    - GUI ?

---

2024년 2월 1일

# Detection Part 사전 조사

- Detection : Car(차선 이탈, 고장, 멈춤, 미끄러짐), Human

멈춤 : car detection 후 이동 감지 → 길이 막히면?

차선 이탈 : lane center detection → car, lane 거리로 이탈 감지(?) → CCTV 각도가 어떤지 중요

고장 : car 가장 바깥라인 밖으로 차가 오래 동안 멈춰있으면

미끄러짐 : ?

Human detection : lane detection → 가장 바깥 라인 안쪽에서 사람 감지 경고

- Weather : Snow, Rain, Fog
    1. 데이터
    - [AI-HUB CCTV 기반 차량정보 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=71573) ( 날씨가 메인 아님 )
        - 데이터 : CCTV 각도에서 촬영되었으나 도시 배경이 대다수
            - 날씨
                
                
                | 날씨 구분 | 맑음(S) | 강우(R) | 안개(F) | 합계 |
                | --- | --- | --- | --- | --- |
                | 구축량 | 855,602장 | 142,495장 | 9,122장 | 1,007,219장 |
                | 구축 비율 | 84.9% | 14.1% | 0.9% | 100% |
            - 시간대
                
                
                | 구분 | 심야 | 오전 | 오후 | 저녁 | 합계 |
                | --- | --- | --- | --- | --- | --- |
                | 구축량 | 36,144장 | 401,501장 | 404,044장 | 165,530장 | 1,007,219장 |
                | 구축 비율 | 3.6% | 39.9% | 40.1% | 16.4% | 100% |
            - 샘플 이미지
        
        ![C-221009_13_CR06_01_N4544.jpg](https://prod-files-secure.s3.us-west-2.amazonaws.com/d10e0519-c0eb-462b-9fce-35c5338cbc45/4654d142-2884-4aab-b14a-494189ebd729/C-221009_13_CR06_01_N4544.jpg)
        
        - [5개 클래스 날씨 이미지 데이터](https://ieee-dataport.org/documents/five-class-weather-image-dataset?page=2#files)
            - 날씨 [:](https://www.kaggle.com/datasets/ammaralfaifi/5class-weather-status-image-classification) 흐림, 맑음, 안개, 비, 눈
            - 데이터 : 날씨의 형태가 원하는 5개의 이상적인 형태이나 데이터의 수준이 매우 좋지 않으며 CCTV 각도보다는 구글에서 크롤링 한듯한 사진임
            
            ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/d10e0519-c0eb-462b-9fce-35c5338cbc45/ccc9a777-e018-4005-aa90-627dad919a40/Untitled.png)
            
            | 구분 | cloudy | foggy | rainy | snowy | sunny | 합계 |
            | --- | --- | --- | --- | --- | --- | --- |
            | 개수 | 6702 | 1261 | 1927 | 1875 | 6274 | 15000 |
        
        - [kaggle 날씨, 시간 예측 데이터](https://www.kaggle.com/datasets/wjybuqi/weathertime-classification-with-road-images/data) ( 차량 시선 기준 )
            - 날씨 : cloudy, sunny, rainy
            - 데이터 : 날씨 구분에 눈이나 안개가 필요해 보임, 차량 기준 사진 데이터
            
            ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/d10e0519-c0eb-462b-9fce-35c5338cbc45/54b78a29-380c-422a-8fc9-9418e6563a49/Untitled.png)
            
            | 구분 | cloudy | sunny | rainy | 합계 |
            | --- | --- | --- | --- | --- |
            | 개수 | 1119 | 886 | 595 | 2600 |
            - 시간대
                
                
                | 구분 | Morning | Afternoon | Dusk | Dawn |
                | --- | --- | --- | --- | --- |
                | 개수 | 1613 | 829 | 124 | 34 |
        
        - [국제교통과학기술저널 도로 표면 날씨 데이터](https://www.sciencedirect.com/science/article/pii/S2046043021000526)
            - 날씨 : dry, snowy, slushy, clear, Light Snow, Havy Snow
            - 데이터 : 바닥면 위주로 보는 데이터
            - 우리나라와 맞지 않는 기상
        - [AI-HUB 승용 자율주행차 악천후 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=data&dataSetSn=630) ( 주행 중 데이터 )
            - 날씨 : 맑음, 우천, 안개, 역광, 우설
            - Lidar + 카메라 데이터
                - Lidar 데이터 pcd file 시각화 test
            - 자율주행 타겟 데이터로 사용이 어려울듯함
            - 데이터 : 좌우앞의 데이터로 분리되어있으며 차량기준의 데이터임
        - [Roboflow weather classification data](https://universe.roboflow.com/search?q=weather) (ajax 웹사이트)
            - 날씨 : Cloudy, Rain, Shine, Sunrise, Tornado
            - 날씨 예측이 될만한 하늘을 바라본 사진임
    
    1. 학습 모델
    - CNN
        - RESNET - 데이터에 과적합 → DenseNet
            - CCTV 데이터 사용 시
        - GoogLeNet - InceptionNet - 경사하강 소실 과다
            - CCTV 가 아닌 이외의 데이터 사용 시
        - efficientnet_pytorch → 사용자의 환경을 확인해야함(?) →멀티 클래스에 유리함
            - 정확도가 좋으나 리소스 많이 사용, 확인 필요

1. 학습 진행
    - 데이터 선택
        - [AI-HUB CCTV 기반 차량정보 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=71573)
    - EDA
        - 날씨 : 맑음 855.602(84.9%)장, 강우 142,495장(14.1%), 안개 9,122장(0.9%)
        - 시간 : 심야 36,144(4%), 오전 401,501(40%), 오후 404,044(40%), 저녁 165,530(16%)
        - train : image
        - label : weather, time, ~~season~~
    - 학습 모델 선택
        - CNN RESNET
    - 검증 방법
        - F1 score, Acc
    - 결과
        - 정확도
        - 학습 시간