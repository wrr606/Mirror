from PyQt5 import QtCore, QtGui, QtWidgets
from FaceID import sign_up,identify
import sys, cv2, threading
from PyQt5.QtCore import QTimer
import psutil
import GPUtil
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Volume import set_volume
from Weather import Weather
import json
with open('city.json', 'r', encoding='utf-8') as file:
    city = json.load(file)
firsttext="金門縣"
join=1
class Ui_Widget(object):
    def __init__(self):
        self.video_thread = None
        plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
        plt.rcParams["axes.unicode_minus"] = False
    #不用理
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1272, 600)
        #登入畫面
#######################################################################
        self.loginpage = QtWidgets.QFrame(Widget)
        self.loginpage.setGeometry(QtCore.QRect(0, 1000, 1271, 601))
        self.loginpage.setStyleSheet("background-color:white;")
        self.loginpage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.loginpage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.loginpage.setObjectName("frame")
        self.graphicshome = QtWidgets.QGraphicsView(self.loginpage)
        self.graphicshome.setGeometry(QtCore.QRect(370, 45, 512, 512))
        self.graphicshome.setObjectName("graphicsHome")
        self.graphicshome.setStyleSheet("border:0;")
        self.scene=QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(245, 250, 10, 10)
        img =QtGui.QPixmap("image/face-id.png")
        self.scene.addPixmap(img)
        self.graphicshome.setScene(self.scene)
        self.user = QtWidgets.QPushButton(self.loginpage)
        self.user.setGeometry(QtCore.QRect(40, 120, 60, 60))
        self.user.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/user 1.png\")"
        )
        self.user.setText("")
        self.user.setObjectName("user")
        self.user.clicked.connect(self.userlogin)
        self.useradd = QtWidgets.QPushButton(self.loginpage)
        self.useradd.setGeometry(QtCore.QRect(40, 200, 60, 60))
        self.useradd.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/user-add.png\")"
        )
        self.useradd.setText("")
        self.useradd.setObjectName("useradd")
        self.useradd.clicked.connect(self.add)
        self.label = QtWidgets.QLabel(self.loginpage)
        self.label.setGeometry(QtCore.QRect(130, 140, 101, 31))
        self.label.setStyleSheet("font-size:25px;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.loginpage)
        self.label_2.setGeometry(QtCore.QRect(130, 220, 101, 31))
        self.label_2.setStyleSheet("font-size:25px;")
        self.label_2.setObjectName("label_2")
        self.camera = QtWidgets.QLabel(self.loginpage)
        self.camera.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.camera.setText("")
        self.camera.setObjectName("camera")
        self.home1 = QtWidgets.QPushButton(self.loginpage)
        self.home1.setGeometry(QtCore.QRect(40, 40, 60, 60))
        self.home1.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/home.png\")"
        )
        self.home1.setText("")
        self.home1.setObjectName("home")
        self.home1.clicked.connect(self.home)
        self.label_3 = QtWidgets.QLabel(self.loginpage)
        self.label_3.setGeometry(QtCore.QRect(130, 60, 101, 31))
        self.label_3.setStyleSheet("font-size:25px;")
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.loginpage)
        self.lineEdit.setGeometry(QtCore.QRect(930, 1000, 211, 61))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("font-size:25px;")
        self.label_4 = QtWidgets.QLabel(self.loginpage)
        self.label_4.setGeometry(QtCore.QRect(930, 1000, 231, 31))
        self.label_4.setStyleSheet("font-size:25px;")
        self.label_4.setObjectName("label_4")
        self.Tick = QtWidgets.QPushButton(self.loginpage)
        self.Tick.setGeometry(QtCore.QRect(1160, 1000, 60, 60))
        self.Tick.clicked.connect(self.check)       
        self.Tick.setStyleSheet(
            "border-radius: 12px;\n"
            "background-repeat: no-repeat;"
            "background-image:url(\"image/check.png\")"
        )
        self.Tick.setObjectName("Tick")
#######################################################################   
        #進入後畫面 
        self.homepage = QtWidgets.QFrame(Widget)
        self.homepage.setGeometry(QtCore.QRect(0, 0, 1272, 600))
        self.homepage.setStyleSheet("")
        self.homepage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.homepage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.homepage.setObjectName("homepage")

        self.username = QtWidgets.QLabel(self.homepage)
        self.username.setGeometry(QtCore.QRect(20, 20, 661, 81))
        self.username.setStyleSheet(
            "font-size:35px;\n"
            "background-color:white;"
        )
        self.username.setObjectName("username")
        #音量控制
        self.control = QtWidgets.QFrame(self.homepage)
        self.control.setGeometry(QtCore.QRect(710, 500, 541, 71))
        self.control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.control.setFrameShadow(QtWidgets.QFrame.Raised)
        self.control.setObjectName("control")
        self.volume = QtWidgets.QLabel(self.control)
        self.volume.setGeometry(QtCore.QRect(10, 10, 50, 50))
        self.volume.setStyleSheet(
            "background-image:url(\"image/volume.png\")"
        )
        self.volume.setObjectName("volume")
        self.volumeslider = QtWidgets.QSlider(self.control)
        self.volumeslider.setGeometry(QtCore.QRect(80, 30, 431, 21))
        self.volumeslider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeslider.setObjectName("volumeslider")
        self.volumeslider.setMinimum(0)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(50)
        self.volumeslider.valueChanged.connect(self.slider)
        #CPU使用率
        self.cpu = QtWidgets.QFrame(self.homepage)
        self.cpu.setGeometry(QtCore.QRect(20, 104, 400, 240))
        self.cpu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cpu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cpu.setObjectName("cpu")
        self.figure_cpu, self.ax_cpu = plt.subplots()
        self.canvas_cpu = FigureCanvas(self.figure_cpu)
        self.canvas_cpu.setFixedSize(400, 200)
        self.cpu_usage_data = [0] * 50  # 初始化 50 筆數據，初始值為 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cpu_usage)
        self.timer.start(100)  # 更新間隔：1000 毫秒（1 秒）
        self.graphicsView_cpu = QtWidgets.QGraphicsView(self.cpu)
        self.graphicsView_cpu.setGeometry(QtCore.QRect(0, 39, 400, 200))
        self.graphicsView_cpu.setObjectName("graphicsView_cpu")
        self.scene_cpu=QtWidgets.QGraphicsScene()
        self.scene_cpu.setSceneRect(15, 0, 350, 195)
        self.scene_cpu.addWidget(self.canvas_cpu)
        self.graphicsView_cpu.setScene(self.scene_cpu)
        self.cpuname = QtWidgets.QLabel(self.cpu)
        self.cpuname.setGeometry(QtCore.QRect(10, 0, 301, 51))
        self.cpuname.setStyleSheet("font-size:30px;")
        self.cpuname.setObjectName("cpuname")
        #GPU使用率
        self.gpu = QtWidgets.QFrame(self.homepage)
        self.gpu.setGeometry(QtCore.QRect(20, 344, 400, 241))
        self.gpu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.gpu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gpu.setObjectName("gpu")
        self.figure_gpu, self.ax_gpu = plt.subplots()
        self.canvas_gpu = FigureCanvas(self.figure_gpu)
        self.canvas_gpu.setFixedSize(400, 200)
        self.gpu_usage_data = [0] * 50  # 初始化 50 筆數據，初始值為 0
        self.timer.timeout.connect(self.update_gpu_usage)
        self.timer.start(1000)
        self.graphicsView_gpu = QtWidgets.QGraphicsView(self.gpu)
        self.graphicsView_gpu.setGeometry(QtCore.QRect(0, 40, 400, 201))
        self.graphicsView_gpu.setObjectName("graphicsView_gpu")
        self.scene_gpu=QtWidgets.QGraphicsScene()
        self.scene_gpu.setSceneRect(15, 10, 350, 180)
        self.scene_gpu.addWidget(self.canvas_gpu)
        self.graphicsView_gpu.setScene(self.scene_gpu)
        self.gpuname = QtWidgets.QLabel(self.gpu)
        self.gpuname.setGeometry(QtCore.QRect(0, 0, 301, 51))
        self.gpuname.setStyleSheet("font-size:30px;")
        self.gpuname.setObjectName("gpuname")
        #相機
        self.userface = QtWidgets.QFrame(self.homepage)
        self.userface.setGeometry(QtCore.QRect(710, 20, 531, 211))
        self.userface.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.userface.setFrameShadow(QtWidgets.QFrame.Raised)
        self.userface.setObjectName("userface")
        self.facecamera = QtWidgets.QLabel(self.userface)
        self.facecamera.setGeometry(QtCore.QRect(0, 0, 531, 211))
        self.facecamera.setObjectName("facecamera")
        #天氣
        self.weather = QtWidgets.QFrame(self.homepage)
        self.weather.setGeometry(QtCore.QRect(440, 110, 261, 201))
        self.weather.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.weather.setFrameShadow(QtWidgets.QFrame.Raised)
        self.weather.setObjectName("weather")
        self.city = QtWidgets.QComboBox(self.weather)
        self.city.setGeometry(QtCore.QRect(20, 20, 101, 22))
        self.city.setObjectName("city")
        self.city.addItems(["金門縣","臺南市","高雄市","新北市","臺北市","宜蘭縣","基隆市","桃園市","新竹市","新竹縣","苗栗縣","臺中市","彰化縣","雲林縣","嘉義縣","臺東縣","連江縣","澎湖縣","屏東縣", "花蓮縣","南投縣","嘉義市"])
        self.city.currentIndexChanged.connect(self.changetown)
        self.township = QtWidgets.QComboBox(self.weather)
        self.township.setGeometry(QtCore.QRect(140, 20, 101, 22))
        self.township.setObjectName("township")
        self.township.addItems(["金沙鎮","金寧鄉","烏坵鄉"])
        self.township.currentIndexChanged.connect(self.changetext)
        self.temperature = QtWidgets.QLabel(self.weather)
        self.temperature.setGeometry(QtCore.QRect(20, 60, 81, 61))
        self.temperature.setStyleSheet("background-color:white;")
        self.temperature.setObjectName("temperature")
        self.weatherimage = QtWidgets.QLabel(self.weather)
        self.weatherimage.setGeometry(QtCore.QRect(120, 60, 121, 121))
        self.weatherimage.setStyleSheet("background-color:white;")
        self.weatherimage.setObjectName("weatherimage")
        self.status = QtWidgets.QLabel(self.weather)
        self.status.setGeometry(QtCore.QRect(20, 150, 81, 31))
        self.status.setStyleSheet("background-color:white;")
        self.status.setObjectName("status")
        #ChatGpt
        self.chatgpt = QtWidgets.QFrame(self.homepage)
        self.chatgpt.setGeometry(QtCore.QRect(710, 240, 531, 80))
        self.chatgpt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chatgpt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chatgpt.setObjectName("chatgpt")
        self.gpt = QtWidgets.QLabel(self.chatgpt)
        self.gpt.setGeometry(QtCore.QRect(0, 0, 531, 80))
        self.gpt.setObjectName("gpt")
        #新聞
        self.news = QtWidgets.QFrame(self.homepage)
        self.news.setGeometry(QtCore.QRect(710, 330, 531, 151))
        self.news.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.news.setFrameShadow(QtWidgets.QFrame.Raised)
        self.news.setObjectName("news")
        self.newslist = QtWidgets.QListWidget(self.news)
        self.newslist.setGeometry(QtCore.QRect(0, 0, 531, 151))
        self.newslist.setObjectName("newslist")
        #代辦事項
        self.list = QtWidgets.QListWidget(self.homepage)
        self.list.setGeometry(QtCore.QRect(440, 320, 261, 211))
        self.list.setObjectName("list")
        self.listdel = QtWidgets.QPushButton(self.homepage)
        self.listdel.setGeometry(QtCore.QRect(470, 540, 93, 31))
        self.listdel.setObjectName("listdel")
        self.listadd = QtWidgets.QPushButton(self.homepage)
        self.listadd.setGeometry(QtCore.QRect(590, 540, 93, 31))
        self.listadd.setObjectName("listadd")

        self.homepage.raise_()
        self.loginpage.raise_()
        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.label.setText(_translate("Widget", "登入"))
        self.label_2.setText(_translate("Widget", "新增用戶"))
        self.label_3.setText(_translate("Widget", "首頁"))
        self.label_4.setText(_translate("Widget", "請輸入你用戶名稱:"))
        self.username.setText(_translate("Widget", "使用者名稱"))
        self.cpuname.setText(_translate("Widget", "CPU使用率(%):"))
        self.gpuname.setText(_translate("Widget", "GPU使用率(%):"))
        self.listdel.setText(_translate("Widget", "刪除"))
        self.listadd.setText(_translate("Widget", "新增"))
        self.temperature.setText(_translate("Widget", "溫度"))
        self.weatherimage.setText(_translate("Widget", "TextLabel"))
        self.facecamera.setText(_translate("Widget", "TextLabel"))
        self.gpt.setText(_translate("Widget", "CHATGPT"))
        self.status.setText(_translate("Widget", "TextLabel"))

#------------以上都是介面---------
        #打開攝像頭
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
        cap.release()    
            #用戶登入
    def userlogin(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.camera.setGeometry(QtCore.QRect(370, 45, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(930, 1000, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(930, 1000, 231, 31))
        self.Tick.setGeometry(QtCore.QRect(1160, 1000, 71, 61))
        self.ocv = True
        # 检查线程是否已经启动
        if not self.video_thread or not self.video_thread.is_alive():
            self.video_thread = threading.Thread(target=self.opencv)
            self.video_thread.start()
        #判斷是不是本人    
        ID=identify()
        if bool(ID)==False :
            #顯示彈窗
            self.err()
        else :
            print(f"歡迎{ID}進入")#liu

    def home(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 45, 512, 512))
        self.camera.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(930, 1000, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(930, 1000, 231, 31))
        self.Tick.setGeometry(QtCore.QRect(1160, 1000, 71, 61))
        self.ocv = False

    def add(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.camera.setGeometry(QtCore.QRect(370, 45, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(930, 140, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(930, 90, 231, 31))
        self.Tick.setGeometry(QtCore.QRect(1160, 140, 71, 61))
        self.ocv = True
        # 检查线程是否已经启动
        if not self.video_thread or not self.video_thread.is_alive():
            self.video_thread = threading.Thread(target=self.opencv)
            self.video_thread.start()

    #check是打勾按鈕
    def check(self):
        if sign_up(self.lineEdit.text()) == False :
            #顯示彈窗
            self.err()
        else :
            print("進入主畫面") #liu
    #顯示彈窗
    def err(self):
        mbox = QtWidgets.QMessageBox(self.frame)
        mbox.setText("請重新操作")
        mbox.setIcon(2)
        mbox.exec()

    #顯示CPU
    def update_cpu_usage(self):
        cpu_usage = min(psutil.cpu_percent(interval=0.1), 100)
        self.cpu_usage_data.append(cpu_usage)
        if len(self.cpu_usage_data) > 50:
            self.cpu_usage_data.pop(0)
        self.ax_cpu.clear()
        self.ax_cpu.bar(range(len(self.cpu_usage_data)), self.cpu_usage_data, color='blue')
        self.ax_cpu.set_ylim([0,100])
        self.ax_cpu.set_xticks([])
        self.canvas_cpu.draw()
    #顯示GPU
    def update_gpu_usage(self):
        gpu = GPUtil.getGPUs()[0]
        gpu_usage = min(gpu.load * 100, 100)
        self.gpu_usage_data.append(gpu_usage)
        if len(self.gpu_usage_data) > 50:
            self.gpu_usage_data.pop(0)
        self.ax_gpu.clear()
        self.ax_gpu.bar(range(len(self.gpu_usage_data)), self.gpu_usage_data, color='green')
        self.ax_gpu.set_ylim([0, 100])
        self.ax_gpu.set_xticks([])
        self.canvas_gpu.draw()
    #切換鄉鎮
    def changetown(self):
        global firsttext,join
        join=0 
        if (self.city.currentText()==firsttext):
            return
        else:
            length=len(self.township) 
            for i in range(0,length):
                self.township.removeItem(0)
            join=1
            firsttext=self.city.currentText()
            self.township.addItems(city[firsttext])
        x=Weather()
        result=x.query(firsttext,self.township.currentText())
        temperature_value, weather_description = result
        self.temperature.setText(temperature_value)
        self.status.setText(weather_description)

        
    def changetext(self):
        if join==1:
            x=Weather()
            result=x.query(firsttext,self.township.currentText())
            temperature_value, weather_description = result
            self.temperature.setText(temperature_value)
            self.status.setText(weather_description)
            print(firsttext,self.township.currentText())
            print("temperature Value:", temperature_value)
            print("Weather Description:", weather_description)  


    # slider 改變value
    def slider(self,value) :
        set_volume(value/100)
        if value==0:
            self.volume.setStyleSheet(
            "background-image:url(\"image/volume-slash.png\")"
        )
        else:
            self.volume.setStyleSheet(
            "background-image:url(\"image/volume.png\")"
        )


        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    video = threading.Thread(target=ui.opencv)  
    Widget.show()
    sys.exit(app.exec_())
