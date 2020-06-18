# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-30 17:03:04
@Desc: 
"""

import cv2
import os
import time
import platform
import threading
import time

STOP = 0
PLAY = 1
PAUSE = 2


class CVideo(threading.Thread):
    def __init__(self):
        super(CVideo, self).__init__()
        self.m_CharList = []
        self.m_Cmd = ""
        self.m_Staue = STOP
        self.m_Path = None
        self.setDaemon(True)
        self._InitData()

    def _InitData(self):
        txt = ""
        for x in range(33, 127):
            txt += chr(x)
        self.m_CharList = list(txt)

        if platform.system() == "Windows":
            self.m_Cmd = "cls"
        else:
            self.m_Cmd = "clear"

    def SetPath(self, sPath):
        self.m_Path = sPath
        self.m_Staue = PLAY

    def Stop(self):
        self.m_Staue = STOP

    def PauseOrContinue(self):
        if self.m_Staue == STOP:
            return
        if self.m_Staue == PLAY:
            self.m_Staue = PAUSE
        else:
            self.m_Staue = PLAY

    def GetStatue(self):
        return self.m_Staue

    def run(self):
        cap = cv2.VideoCapture(self.m_Path)
        iBegin = time.time()
        iTime = 0
        iFrame = 0
        while True:
            if self.m_Staue == STOP:
                break
            if self.m_Staue == PAUSE:
                time.sleep(0.01)
                continue
            hasFrame, frame = cap.read()
            if not hasFrame:
                break
            width = frame.shape[0]
            height = frame.shape[1]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            size = cv2.resize(gray, (width//10, height//10))
            os.system(self.m_Cmd)
            txt = ""
            for row in size:
                for pix in row:
                    txt += self.m_CharList[pix * len(self.m_CharList) // 256]
                txt += "\n"
            print(txt)
            t = 1.0 / 30    # 设置每秒30帧，还是不能保持同步
            time.sleep(t)
            iTime += t
            iFrame += 1

        print("花费时长:%s 理论时长:%s 帧数:%s" % (time.time()-iBegin, iTime, iFrame))
