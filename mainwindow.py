# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-30 16:56:19
@Desc: cmd 命令行播放器
"""

import os
import video

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton,\
    QHBoxLayout, QVBoxLayout, QDoubleSpinBox, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap


class CMainWindow(QWidget):
    m_Filter = "*.mp4 *.MP4"
    m_Dict = {
        "start": "开始",
        "stop": "停止",
        "pause": "暂停",
        "continue": "继续",
    }

    def __init__(self, parent=None):
        super(CMainWindow, self).__init__(parent)
        self.m_LineEdit = None
        self.m_SelectBtn = None
        self.m_StartBtn = None
        self.m_StopBtn = None
        self.m_PauseBtn = None
        self.m_Rate = None
        self.m_Video = video.CVideo()
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        vBox = QVBoxLayout(self)
        hBox1 = QHBoxLayout()
        lable = QLabel("选择视频", self)
        self.m_LineEdit = QLineEdit(self)
        self.m_LineEdit.setReadOnly(True)
        self.m_SelectBtn = QPushButton("...", self)
        hBox1.addWidget(lable)
        hBox1.addWidget(self.m_LineEdit)
        hBox1.addWidget(self.m_SelectBtn)

        hBox2 = QHBoxLayout()
        lable = QLabel("播放速率", self)
        self.m_Rate = QDoubleSpinBox(self)
        self.m_Rate.setValue(1.0)
        hBox2.addWidget(lable)
        hBox2.addWidget(self.m_Rate)

        hBox3 = QHBoxLayout()
        self.m_StartBtn = self._GetBtn("start")
        self.m_StopBtn = self._GetBtn("stop")
        self.m_PauseBtn = self._GetBtn("pause")
        hBox3.addWidget(self.m_StartBtn)
        hBox3.addWidget(self.m_StopBtn)
        hBox3.addWidget(self.m_PauseBtn)

        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)
        vBox.addLayout(hBox3)

        self._RefreshStatue()

    def _GetBtn(self, sIcon):
        btn = QPushButton(self)
        self._SetBtnIcon(btn, sIcon)
        return btn

    def _SetBtnIcon(self, btn, sIcon):
        sName = self.m_Dict[sIcon]
        btn.setText(sName)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon/%s.png" % sIcon), QIcon.Normal, QIcon.Off)
        btn.setIcon(icon)

    def _InitSignal(self):
        self.m_SelectBtn.clicked.connect(self.S_SelectVideo)
        self.m_StartBtn.clicked.connect(self.S_StartVideo)
        self.m_StopBtn.clicked.connect(self.S_StopVideo)
        self.m_PauseBtn.clicked.connect(self.S_PauseVideo)

    def S_SelectVideo(self):
        sPath = QFileDialog.getOpenFileName(self, "选择视频", filter=self.m_Filter)[0]
        if sPath:
            self.m_LineEdit.setText(sPath)

    def S_StartVideo(self):
        sPath = self.m_LineEdit.text()
        if not os.path.exists(sPath):
            return
        self.m_Video = video.CVideo()
        self.m_Video.SetPath(sPath)
        self.m_Video.start()
        self._RefreshStatue()

    def _RefreshStatue(self):
        iStatue = self.m_Video.GetStatue()
        if iStatue == video.STOP:
            self.m_StartBtn.show()
            self.m_StopBtn.hide()
            self.m_PauseBtn.hide()
            self._SetBtnIcon(self.m_StartBtn, "start")
            return

        if iStatue == video.PLAY:
            self.m_StartBtn.hide()
            self.m_StopBtn.show()
            self.m_PauseBtn.show()
            self._SetBtnIcon(self.m_StopBtn, "stop")
            self._SetBtnIcon(self.m_PauseBtn, "pause")
            return

        if iStatue == video.PAUSE:
            self.m_StartBtn.hide()
            self.m_StopBtn.show()
            self.m_PauseBtn.show()
            self._SetBtnIcon(self.m_StopBtn, "stop")
            self._SetBtnIcon(self.m_PauseBtn, "continue")
            return

    def S_StopVideo(self):
        self.m_Video.Stop()
        self._RefreshStatue()

    def S_PauseVideo(self):
        self.m_Video.PauseOrContinue()
        self._RefreshStatue()
