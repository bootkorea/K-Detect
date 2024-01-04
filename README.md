# K-Detect

K-Detect는 전동 킥보드 이용에 관한 실시간/녹화 영상을 분석하여, 불법 이용 여부의 판독을 돕는 프로그램입니다.

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
