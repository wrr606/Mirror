# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import sys, cv2, threading


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1272, 600)
        self.frame = QtWidgets.QFrame(Widget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1271, 601))
        self.frame.setStyleSheet("background-color:white;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.graphicshome = QtWidgets.QGraphicsView(self.frame)
        self.graphicshome.setGeometry(QtCore.QRect(370, 45, 512, 512))
        self.graphicshome.setObjectName("graphicsHome")
        self.graphicshome.setStyleSheet("border:0;")
        self.scene=QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(245, 250, 10, 10)
        img =QtGui.QPixmap("image/face-id.png")
        self.scene.addPixmap(img)
        self.graphicshome.setScene(self.scene)
        self.user = QtWidgets.QPushButton(self.frame)
        self.user.setGeometry(QtCore.QRect(40, 120, 60, 60))
        self.user.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/user 1.png\")"
        )
        self.user.setText("")
        self.user.setObjectName("user")
        self.user.clicked.connect(self.userlogin)
        self.useradd = QtWidgets.QPushButton(self.frame)
        self.useradd.setGeometry(QtCore.QRect(40, 200, 60, 60))
        self.useradd.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/user-add.png\")"
        )
        self.useradd.setText("")
        self.useradd.setObjectName("useradd")
        self.useradd.clicked.connect(self.add)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(130, 140, 101, 31))
        self.label.setStyleSheet("font-size:25px;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(130, 220, 101, 31))
        self.label_2.setStyleSheet("font-size:25px;")
        self.label_2.setObjectName("label_2")
        self.camera = QtWidgets.QLabel(self.frame)
        self.camera.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.camera.setText("")
        self.camera.setObjectName("camera")
        self.home1 = QtWidgets.QPushButton(self.frame)
        self.home1.setGeometry(QtCore.QRect(40, 40, 60, 60))
        self.home1.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/home.png\")"
        )
        self.home1.setText("")
        self.home1.setObjectName("home")
        self.home1.clicked.connect(self.home)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(130, 60, 101, 31))
        self.label_3.setStyleSheet("font-size:25px;")
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(930, 1000, 211, 61))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("font-size:25px;")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(930, 1000, 231, 31))
        self.label_4.setStyleSheet("font-size:25px;")
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(1160, 1000, 60, 60))
        self.pushButton.setStyleSheet(
            "border-radius: 12px;\n"
            "background-repeat: no-repeat;"
            "background-image:url(\"image/check.png\")"
        )
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.label.setText(_translate("Widget", "登入"))
        self.label_2.setText(_translate("Widget", "新增用戶"))
        self.label_3.setText(_translate("Widget", "首頁"))
        self.label_4.setText(_translate("Widget", "請輸入你用戶名稱:"))

    def opencv(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while self.ocv:
            ret, frame = cap.read()
            if not ret:
                print("Cannot receive frame")
                break
            frame = cv2.resize(frame, (480, 320))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytesPerline = channel * width
            qimg = QImage(frame, width, height, bytesPerline, QImage.Format_RGB888)
            self.camera.setPixmap(QPixmap.fromImage(qimg)) 

    def userlogin(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.camera.setGeometry(QtCore.QRect(370, 45, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(930, 1000, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(930, 1000, 231, 31))
        self.pushButton.setGeometry(QtCore.QRect(1160, 1000, 71, 61))
        self.ocv = True
        video.start()

    def home(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 45, 512, 512))
        self.camera.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(930, 1000, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(930, 1000, 231, 31))
        self.pushButton.setGeometry(QtCore.QRect(1160, 1000, 71, 61))
        self.ocv = False

    def add(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.camera.setGeometry(QtCore.QRect(370, 45, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(930, 140, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(930, 90, 231, 31))
        self.pushButton.setGeometry(QtCore.QRect(1160, 140, 71, 61))
        
        self.ocv = True
        video.start()
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    video = threading.Thread(target=ui.opencv)
    
    Widget.show()
    sys.exit(app.exec_())