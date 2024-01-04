from ultralytics import YOLO
import cv2
import math
import numpy as np
import torch

check_id = [30, 31, 32, 33, 35, 36]  # 불법 탐지 id


class Detection:
    def __init__(self):
        # model
        self.model = YOLO("./model/best.pt")

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(device)

        # 클래스에 따른 임계값 설정
        self.class_thresholds = {
            30: 0.4,
            31: 0.6,
            32: 0.25,
            33: 0.2,
            35: 0.3,
            36: 0.25
        }

    def detect(self, img):
        res = np.array([0, 0, 0, 0, 0, 0])  # 6개 클래스에 대한 결과를 저장할 배열 선언
        w, h, c = img.shape

        # 이미지 크기 조정
        if w > 1920:
            img = cv2.resize(img, (1920, h))
        if h > 1080:
            img = cv2.resize(img, (w, 1080))

        # 모델 Prediction
        results = self.model(img, stream=True)

        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100

                # Check if confidence is above the threshold for the class
                res_cls = int(box.cls[0])  # 이미 각 박스에 대한 cls이므로 0번째 인덱스를 취함
                if confidence >= self.class_thresholds.get(res_cls, 0.15):
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(
                        x2), int(y2)  # convert to int values

                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    print("Confidence --->", confidence)

                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2
                    res_cls = int(box.cls[0])  # 이미 각 박스에 대한 cls이므로 0번째 인덱스를 취함
                    cv2.putText(
                        img, f"Class: {res_cls}", org, font, fontScale, color, thickness)
                    # 결과로 나온 바운딩 각 박스들의 클래스에 따라 결과배열의 해당인덱스에 카운팅

                    if res_cls in check_id:
                        index = check_id.index(res_cls)
                        res[index] += 1

        return img, res
