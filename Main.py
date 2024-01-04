import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic
import threading
import cv2
from Detection import Detection
from queue import Queue
import numpy as np
import pygame
import time

form_class = uic.loadUiType("CheckManager.ui")[0]


# 각종 버튼 및 메뉴 메소드 구현 1.종료 2.키보드 입력 3.적용 4.초기화 5.설정 저장/불러오기 6.비디오 변경
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        # 웹 캠 경우
        # self.cap = cv2.VideoCapture(0)
        # 영상 로드 경우
        self.cap = cv2.VideoCapture("./media/test.mp4")
        self.detection = Detection()
        self.setupUi(self)
        self.setFixedSize(800, 600)
        self.setWindowTitle("CheckManager")
        self.video_thread()
        self.chk_list = []  # 24프레임 간격으로 저장될 chk 큐
        # 24프레임에 대한 합산된 클래스 개수를 저장할 변수
        self.chk_sum_arr = np.array([0, 0, 0, 0, 0, 0])
        self.passFrames = 0  # 음악 재생할때마다 프레임 갱신
        self.isPlaySound = False

    def video_thread(self):
        self.thread = threading.Thread(target=self.cv_Frame, args=())
        self.thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        self.thread.start()

    def cv_Frame(self):
        prev_time = 0

        while self.cap.isOpened():
            success, img = self.cap.read()
            if success:
                d_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                d_img, chk = self.detection.detect(d_img)
                h, w, c = d_img.shape
                s = self.result_chk(chk)

                current_time = time.time()  # Get the current time
                fps = 1 / (current_time - prev_time)  # Calculate FPS
                prev_time = current_time  # Update the previous time

                print(f"FPS: {fps:.2f}")

                if s:
                    print(f"불법 탐지: {s}")

                # 이미지를 QLabel크기에 맞게 조정하고 QPixmap으로 생성
                label_width = self.videoFrame.width()
                label_height = self.videoFrame.height()

                q_image = QImage(d_img, w, h, QImage.Format_RGB888)
                pixmp = QPixmap.fromImage(q_image)
                pixmp = pixmp.scaled(QSize(label_width, label_height))
                self.videoFrame.setPixmap(pixmp)
                self.videoFrame.resize(pixmp.width(), pixmp.height())

                # 현재 상태, 프레임마다 업데이트
                self.videoFrame.update()
            if cv2.waitKey(14) & 0xFF == 27:  # 27은 ESC 키의 ASCII 코드입니다.
                break

    def result_chk(self, chk):
        if len(self.chk_list) > 24:
            self.chk_sum_arr -= self.chk_list.pop()
            self.chk_list.insert(0, chk)
            self.chk_sum_arr += chk

            print(self.chk_sum_arr)  # 현재 상황

            if self.isPlaySound:
                if self.passFrames < 0:
                    self.isPlaySound = False
                else:
                    self.passFrames -= 1

                arr = self.chk_sum_arr >= 13

                # 재생중일때도, 12이상인 클래스가 검출되면 0으로 초기화
                for idx, val in enumerate(arr):
                    if val == True:
                        self.chk_sum_arr[idx] = 0
                        for i in self.chk_list:
                            i[idx] = 0

                return -1  # 재생 중

            res = self.chk_sum_arr > 12
            for idx, cls_val in enumerate(res):
                if cls_val:  # 특정 클래스에 대해 12번이상 검출된 경우
                    if idx == 2 or idx == 3:  # 32,33번 클래스
                        self.speak("./media/32.wav")
                        self.isPlaySound = True
                        self.passFrames = 2 * 8
                    elif idx == 5:  # 36번 클래스
                        self.speak("./media/36.wav")
                        self.isPlaySound = True
                        self.passFrames = 4 * 8
                    elif idx == 0:  # 30번 클래스
                        self.speak("./media/30.wav")
                        self.isPlaySound = True
                        self.passFrames = 3 * 8
                    elif idx == 4:  # 35번 클래스
                        self.speak("./media/35.wav")
                        self.isPlaySound = True
                        self.passFrames = 2 * 8
                    elif idx == 1:  # 31번 클래스
                        self.speak("./media/31.wav")
                        self.isPlaySound = True
                        self.passFrames = 5 * 8

                    if self.chk_sum_arr[idx] >= 13:
                        self.chk_sum_arr[idx] = 0
                        for i in self.chk_list:
                            i[idx] = 0

                    if self.isPlaySound:
                        return idx
        else:
            self.chk_list.insert(0, chk)
            self.chk_sum_arr += chk

            print(self.chk_sum_arr)  # 현재 상

    def speak(self, file_name):
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_name)
        sound.play()

        # 재생이 끝날 때까지 대기
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
