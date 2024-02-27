# K-Detect
### 교내 전동 킥보드 불법 이용 사례 탐지 및 개선 솔루션

: K-Detect는 전동 킥보드(이하 **PM**) 이용에 관한 실시간/녹화 영상을 분석하여, 불법 이용 여부의 판독을 돕는 프로그램입니다.

---

## 연구 배경

![image](https://github.com/bootkorea/K-Detect/assets/90824684/1fa7b9be-d203-413c-8e56-41b270776036)

+ PM 이용자 수는 해를 거듭하며 증가하고 있음
+ 이용자 수가 증가하면서 지난 5년간 PM 사건건수가 약 10배 이상 증가

![image](https://github.com/bootkorea/K-Detect/assets/90824684/7f4327fc-407a-471d-947e-ef64f1102c0d)

+ '**불법 주정차 문제**'는 제한 구역 설정 및 추가 요금 부과 등의 조치를 통해 성과를 내고 있음
+ 반면 **2인 이상 탑승**, **헬멧 미착용**과 같은 불법 이용 방지 대책은 미흡
  + 캠페인 활동 및 자체 단속을 진행하지만 이는 일시적인 행동 변화를 유도할 뿐, 지속성이 떨어진다는 한계

: **지속 가능**하며 **실현**할 수 있는 솔루션 제안

---

## 작품 개요

![image](https://github.com/bootkorea/K-Detect/assets/90824684/1ae5f3b4-6d17-4585-b9bc-f343fed19828)

![image](https://github.com/bootkorea/K-Detect/assets/90824684/a6af513e-1e48-4188-a865-3221aa0b0747)

+ 교내에 **CCTV**와 **스피커**가 다수 설치 되어 있음을 확인, 활용 계획
  + 교내 설치되어있는 자산을 활용해 초기 비용 절감

+ 특정 영역을 지속적으로 감시하며 실시간으로 일어나고 있는 일을 영상 이미지 형태로 저장하는 특성을 지닌 CCTV
  + CCTV 영상 이미지를 이용하기 위해 실시간 객체 탐지 모델인 [YOLOv8](https://github.com/ultralytics/ultralytics)을 활용  

+ 교내에서 많이 발생하는 불법 이용 사례를 유형화하여 모델을 학습
+ 학습한 모델을 바탕으로 PM 불법 이용 상황이 인식되는 즉시 경각심을 일깨우기 위해 교내에 설치된 스피커에서 '_경고 음성 메세지_' 출력
  + 음성 경고 알림은 '_쓰레기 무단투기에 대한 스마트 경고 시스템_'의 성공 사례를 통해 효과가 있음을 입증

---

## 불법 탐지 구현

![image](https://github.com/bootkorea/K-Detect/assets/90824684/39c48cde-7fd5-4c98-9140-a5f9875f4711)

+ 학습데이터: AI-HUB에 공개된 [데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=614) 활용
  + train: 71,986장
  + val: 15,421장
  + test: 15,420장
    + 교내 도로에서 PM 이용 사례를 연출하여 영상 이미지 수집
    + 학습된 모델과 연계하여 불법 이용 검출 결과 확인

+ 불법 탐지 프로그램
  + Webcam View: 실시간 영상 이미지 제공
  + PyQT
    + 실시간 영상 이미지 연동, 학습한 AI 모델을 활용해 불법 사례 판별
    + 추출한 정보 가공: 어떤 붋법 탐지를 했는지에 대한 정보 / 불법 탐지 시점 / 불법 탐지 연속 이미지  

---

## 한계점 & 개선해야 할 부분

+ 교내에서 불법 이용으로 인한 사례를 확보하는데 어려움
+ 시간 제약으로 인해 많은 학습이 이루어지지 않음
+ 데이터셋의 크기 조절 및 Fine-tunning 과정이 미흡
+ 제도적 한계로 인해 자동차 과속 단속 카메라가 수행하는 기능을 그대로 PM에 적용하여 단속 기능 구현을 못함

---

## 기대효과

![image](https://github.com/bootkorea/K-Detect/assets/90824684/aab33609-76cd-4170-b066-084ef4663ca8)

---

## 파일 구조

- **Detection.py**: 불법 이용 판독 기능 스크립트
- **Main.py**: 프로그램의 메인 진입점
- **requirements.txt**: 모든 의존성이 나열됩니다. `pip install -r requirements.txt`로 설치하세요
- **CheckManager.ui**: User Interface
- **model/**: 전동 킥보드 이용 및 불법 이용 판독에 필요한 모델을 포함합니다
- **media/**: 프로그램에서 사용되는 영상/이미지 자료

## 실행 방법

1. Local 환경에 Python3 설치.
2. Dependencies 설치: `pip install -r requirements.txt`
3. 프로그램 실행: `python Main.py`

## Dependencies

pip 패키지 관리자를 이용하여 `requirements.txt` 파일 설치.
