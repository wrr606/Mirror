from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import sys, threading, json
from time import sleep
from FaceID import sign_up,identify
import cv2
import psutil, GPUtil
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Volume import set_volume,get_volume
from Crawler import News,Weather
from Memorandum import add_district,remove_value
from ChatGPT import chatgpt

with open('city.json', 'r', encoding='utf-8') as file:
    city = json.load(file)
firsttext="金門縣"
join=1

class CPUThread(QThread):
    cpu_updated = pyqtSignal(float)
    def run(self):
        while True:
            cpu_usage = min(psutil.cpu_percent(interval=0.1), 100)
            self.cpu_updated.emit(cpu_usage)
            self.sleep(1)

class GPUThread(QThread):
    gpu_updated = pyqtSignal(float)
    def run(self):
        while True:
            gpu = GPUtil.getGPUs()[0]
            gpu_usage = min(gpu.load * 100, 100)
            self.gpu_updated.emit(gpu_usage)
            self.sleep(1)

class Ui_Widget(object):
    def __init__(self):
        self.video_thread = None
        plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
        plt.rcParams["axes.unicode_minus"] = False
        self.cpu_thread = CPUThread()
        self.cpu_thread.cpu_updated.connect(self.update_cpu_usage)
        self.cpu_thread.start()
        self.gpu_thread = GPUThread()
        self.gpu_thread.gpu_updated.connect(self.update_gpu_usage)
        self.gpu_thread.start()
        self.city_weather=Weather()
        self.line_news=News()
        self.frame=None
        self.ocv=True

    #不用理
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1272, 721)
        #登入畫面
#######################################################################
        self.loginpage = QtWidgets.QFrame(Widget)
        self.loginpage.setGeometry(QtCore.QRect(0, 0, 1272, 721))
        self.loginpage.setStyleSheet("background-color:white;")
        self.loginpage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.loginpage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.loginpage.setObjectName("loginpage")
        self.graphicshome = QtWidgets.QGraphicsView(self.loginpage)
        self.graphicshome.setGeometry(QtCore.QRect(370, 10, 600, 600))
        self.graphicshome.setObjectName("graphicsHome")
        self.graphicshome.setStyleSheet("border:0px;")
        self.scene=QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(10, 10, 595, 595)
        img =QtGui.QPixmap("image/face-id.png")
        self.scene.addPixmap(img)
        self.graphicshome.setScene(self.scene)
        self.user = QtWidgets.QPushButton(self.loginpage)
        self.user.setGeometry(QtCore.QRect(40, 190, 60, 60))
        self.user.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/user 1.png\")"
        )
        self.user.setText("")
        self.user.setObjectName("user")
        self.user.clicked.connect(self.userlogin)
        self.useradd = QtWidgets.QPushButton(self.loginpage)
        self.useradd.setGeometry(QtCore.QRect(40, 280, 60, 60))
        self.useradd.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/user-add.png\")"
        )
        self.useradd.setObjectName("useradd")
        self.useradd.clicked.connect(self.add)
        self.user_text = QtWidgets.QPushButton(self.loginpage)
        self.user_text.setGeometry(QtCore.QRect(130, 210, 101, 31))
        self.user_text.setStyleSheet('''
            font-size:25px;
            border:0px;                        
        ''')
        self.user_text.setObjectName("user_text")
        self.user_text.clicked.connect(self.userlogin)
        self.useradd_text = QtWidgets.QPushButton(self.loginpage)
        self.useradd_text.setGeometry(QtCore.QRect(150, 300, 101, 31))
        self.useradd_text.setStyleSheet('''
            font-size:25px;
            border:0px;                        
        ''')
        self.useradd_text.setObjectName("useradd_text")
        self.useradd_text.clicked.connect(self.add)
        self.home_text = QtWidgets.QPushButton(self.loginpage)
        self.home_text.setGeometry(QtCore.QRect(130, 120, 101, 31))
        self.home_text.setStyleSheet('''
            font-size:25px;
            border:0px;                        
        ''')
        self.home_text.setObjectName("home_text")
        self.home_text.clicked.connect(self.home)
        self.camera = QtWidgets.QLabel(self.loginpage)
        self.camera.setGeometry(QtCore.QRect(350, 1000, 512, 512))
        self.camera.setText("")
        self.camera.setObjectName("camera")
        self.home1 = QtWidgets.QPushButton(self.loginpage)
        self.home1.setGeometry(QtCore.QRect(40, 100, 60, 60))
        self.home1.setStyleSheet(
            "border-radius: 12px;\n"
            "background-image:url(\"image/home.png\")"
        )
        self.home1.setText("")
        self.home1.setObjectName("home")
        self.home1.clicked.connect(self.home)
        self.lineEdit = QtWidgets.QLineEdit(self.loginpage)
        self.lineEdit.setGeometry(QtCore.QRect(920, 1000, 211, 61))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("font-size:25px;")
        self.label_4 = QtWidgets.QLabel(self.loginpage)
        self.label_4.setGeometry(QtCore.QRect(920, 1000, 231, 31))
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
        self.homepage.setGeometry(QtCore.QRect(0, 1000, 1272, 721))
        self.homepage.setStyleSheet("")
        self.homepage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.homepage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.homepage.setObjectName("homepage")
        self.homepage.setStyleSheet('''
            QFrame#homepage{
                background-color:rgb(184,214,214);                        
            }
            QLabel#username{
                font-size:35px;
                background-color:rgb(239,245,245); 
                border-radius:30px;  
                font-family:"DFKai-SB";                    
            } 
        ''')
        self.username = QtWidgets.QLabel(self.homepage)
        self.username.setGeometry(QtCore.QRect(25, 15, 661, 55))
        self.username.setObjectName("username")
        self.username.setAlignment(QtCore.Qt.AlignCenter)
        self.username.setStyleSheet('''
            QLabel#username{
                font-size:35px;
                background-color:rgb(239,245,245); 
                font-family:"DFKai-SB"; 
                font-weight:bold;
                text-align:center;
                border-radius: 15px;                 
            } 
            QLabel#username:hover {
                background-color:rgb(90,177,201);
            }
        ''')
        #音量控制
        self.control = QtWidgets.QFrame(self.homepage)
        self.control.setGeometry(QtCore.QRect(20, 640, 401, 71))
        self.control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.control.setFrameShadow(QtWidgets.QFrame.Raised)
        self.control.setObjectName("control")
        self.control.setStyleSheet('''
            QFrame#control {
                background-color:rgb(239,245,245); 
                border-radius:30px;             
            }
            QFrame#control:hover {
                background-color:rgb(90,177,201);
            }      
            QLabel#volume_text{
                font-size:25px;
                background-color:rgb(239,245,245);                          
            }
            QSlider#volumeslider{
                background-color:rgb(239,245,245);
            }
            QLabel#volume{
                background-image:url(\"image/volume.png\");  
                background-color:rgb(239,245,245);             
            }
        ''')
        self.control.enterEvent = self.control_onEnter
        self.control.leaveEvent = self.control_onLeave
        self.volume = QtWidgets.QLabel(self.control)
        self.volume.setGeometry(QtCore.QRect(10, 10, 50, 50))
        self.volume.setObjectName("volume")
        self.volume_text = QtWidgets.QLabel(self.control)
        self.volume_text.setGeometry(QtCore.QRect(345, 10, 50, 50))
        self.volume_text.setObjectName("volume_text")
        self.volumeslider = QtWidgets.QSlider(self.control)
        self.volumeslider.setGeometry(QtCore.QRect(80, 30, 250, 21))
        self.volumeslider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeslider.setObjectName("volumeslider")
        self.volumeslider.setMinimum(0)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(get_volume())
        self.volume_text.setText(f"{get_volume()}%")
        self.volumeslider.valueChanged.connect(self.slider)
        #CPU使用率
        self.cpu = QtWidgets.QFrame(self.homepage)
        self.cpu.setGeometry(QtCore.QRect(20, 80, 400, 275))
        self.cpu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cpu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cpu.setObjectName("cpu")
        self.cpu.setStyleSheet('''
            QFrame#cpu {
                background-color:rgb(239,245,245); 
                border-radius:30px;             
            }        
            QFrame#cpu:hover {
                background-color:rgb(90,177,201);
            }
            QLabel#cpuname{
                background-color:rgb(239,245,245); 
                border-radius:30px; 
                font-size:30px;         
            }                  
        ''')
        self.cpu.enterEvent = self.cpu_onEnter
        self.cpu.leaveEvent = self.cpu_onLeave
        self.figure_cpu, self.ax_cpu = plt.subplots()
        self.canvas_cpu = FigureCanvas(self.figure_cpu)
        self.canvas_cpu.setFixedSize(350, 200)
        self.cpu_usage_data = [0] * 50  # 初始化 50 筆數據，初始值為 0
        self.graphicsView_cpu = QtWidgets.QGraphicsView(self.cpu)
        self.graphicsView_cpu.setGeometry(QtCore.QRect(20, 45, 350, 201))
        self.graphicsView_cpu.setObjectName("graphicsView_cpu")
        self.scene_cpu=QtWidgets.QGraphicsScene()
        self.scene_cpu.setSceneRect(15, 0, 315, 195)
        self.scene_cpu.addWidget(self.canvas_cpu)
        self.graphicsView_cpu.setScene(self.scene_cpu)
        self.cpuname = QtWidgets.QLabel(self.cpu)
        self.cpuname.setGeometry(QtCore.QRect(20, 0, 301, 41))
        self.cpuname.setObjectName("cpuname")
        #GPU使用率
        self.gpu = QtWidgets.QFrame(self.homepage)
        self.gpu.setGeometry(QtCore.QRect(20, 365, 400, 260))
        self.gpu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.gpu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gpu.setObjectName("gpu")
        self.gpu.setStyleSheet('''
            QFrame#gpu {
                background-color:rgb(239,245,245); 
                border-radius:30px;             
            }        
            QFrame#gpu:hover {
                background-color:rgb(90,177,201);
            }
            QLabel#gpuname{
                background-color:rgb(239,245,245); 
                border-radius:30px; 
                font-size:30px;         
            }
        ''')
        self.gpu.enterEvent = self.gpu_onEnter
        self.gpu.leaveEvent = self.gpu_onLeave
        self.figure_gpu, self.ax_gpu = plt.subplots()
        self.canvas_gpu = FigureCanvas(self.figure_gpu)
        self.canvas_gpu.setFixedSize(350, 200)
        self.gpu_usage_data = [0] * 50  # 初始化 50 筆數據，初始值為 0
        self.graphicsView_gpu = QtWidgets.QGraphicsView(self.gpu)
        self.graphicsView_gpu.setGeometry(QtCore.QRect(25, 40, 350, 201))
        self.graphicsView_gpu.setObjectName("graphicsView_gpu")
        self.scene_gpu=QtWidgets.QGraphicsScene()
        self.scene_gpu.setSceneRect(15, 0, 315, 195)
        self.scene_gpu.addWidget(self.canvas_gpu)
        self.graphicsView_gpu.setScene(self.scene_gpu)
        self.gpuname = QtWidgets.QLabel(self.gpu)
        self.gpuname.setGeometry(QtCore.QRect(25, 5, 301, 31))
        self.gpuname.setObjectName("gpuname")
        #天氣
        self.weather = QtWidgets.QFrame(self.homepage)
        self.weather.setGeometry(QtCore.QRect(440, 90, 261, 201))
        self.weather.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.weather.setFrameShadow(QtWidgets.QFrame.Raised)
        self.weather.setObjectName("weather")
        self.weather.setStyleSheet('''
            QFrame#weather {
                background-color: rgb(239,245,245); 
                border-radius: 30px;             
            }        
            QFrame#weather:hover {
                background-color: rgb(90, 177, 201);
            }
            QLabel {
                background-color: rgb(239,245,245);
                color:rgb(83,103,115);
            }
            QLabel#temperature {
                font-size: 45px;
            }
            QLabel#status {
                font-size: 35px;
            }
            QComboBox {
                background-color: rgb(239, 245, 245);
            }
            QComboBox::drop-down { 
                background-color: rgb(239, 245, 245); 
            }
        ''')
        self.weather.enterEvent = self.weather_onEnter
        self.weather.leaveEvent = self.weather_onLeave
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
        self.temperature.setObjectName("temperature")
        self.weatherimage = QtWidgets.QLabel(self.weather)
        self.weatherimage.setGeometry(QtCore.QRect(120, 60, 121, 121))
        self.weatherimage.setObjectName("weatherimage")
        self.status = QtWidgets.QLabel(self.weather)
        self.status.setGeometry(QtCore.QRect(35, 135, 81, 31))
        self.status.setObjectName("status")
        self.changetext()
        #ChatGpt
        self.chatgpt = QtWidgets.QFrame(self.homepage)
        self.chatgpt.setGeometry(QtCore.QRect(720, 29, 531, 391))
        self.chatgpt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chatgpt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chatgpt.setObjectName("chatgpt")
        self.chatgpt.setStyleSheet('''
            QFrame#chatgpt {
                background-color: rgb(239,245,245); 
                border-radius: 30px; 
            }      
            QFrame#chatgpt:hover {
                background-color: rgb(90, 177, 201);
            }
            QPushButton#chatgpt_check_btn{
                background-color: rgb(241,247,247); 
                border:1px solid #000; 
                border-radius: 10px;  
                font-size:25px;                                 
            }
            QListWidget#gpt {
                border:1px solid #000;
                background-color:white;
                border-radius: 10px; 
                font-size:25px;                      
            }        
            QTextEdit#chatgpt_input{
                border:1px solid #000;
                background-color:white;
                border-radius: 10px; 
                font-size:25px;                       
            }
        ''')
        self.chatgpt_input = QtWidgets.QTextEdit(self.chatgpt)
        self.chatgpt_input.setGeometry(QtCore.QRect(20, 20, 410, 121))
        self.chatgpt_input.setObjectName("chatgpt_input")
        self.gpt = QtWidgets.QListWidget(self.chatgpt)
        self.gpt.setGeometry(QtCore.QRect(20, 160, 490, 210))
        self.gpt.setStyleSheet("background-color:white;")
        self.gpt.setObjectName("gpt")
        self.chatgpt_check_btn = QtWidgets.QPushButton(self.chatgpt)
        self.chatgpt_check_btn.setGeometry(QtCore.QRect(445, 90, 75, 50))
        self.chatgpt_check_btn.setObjectName("chatgpt_check_btn")
        self.chatgpt_check_btn.clicked.connect(self.chatgpt_ans)
        #新聞
        self.news = QtWidgets.QFrame(self.homepage)
        self.news.setGeometry(QtCore.QRect(720, 430, 531, 271))
        self.news.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.news.setFrameShadow(QtWidgets.QFrame.Raised)
        self.news.setObjectName("news")
        self.news.setStyleSheet('''
            QFrame#news {
                background-color: rgb(239,245,245); 
                border-radius: 30px; 
            }      
            QFrame#news:hover {
                background-color: rgb(90, 177, 201);
            }
            QListWidget#newslist {
                border:1px solid #000;
                background-color:white;
                border-radius: 10px;                       
            }  
            QListWidget#newslist{
                font-size:18px;                          
            }                     
        ''')
        self.newslist = QtWidgets.QListWidget(self.news)
        self.newslist.setGeometry(QtCore.QRect(23, 20, 485, 235))
        self.newslist.setObjectName("newslist")
        self.newslist.clicked.connect(self.open_link)
        #代辦事項
        self.list_frame= QtWidgets.QFrame(self.homepage)
        self.list_frame.setGeometry(QtCore.QRect(440, 315, 270, 380))
        self.list_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.list_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.list_frame.setObjectName("list_frame")
        self.list_frame.enterEvent = self.list_onEnter
        self.list_frame.leaveEvent = self.list_onLeave
        self.list_frame.setStyleSheet('''
            QFrame#list_frame {
                background-color: rgb(239,245,245); 
                border-radius: 30px; 
            }      
            QFrame#list_frame:hover {
                background-color: rgb(90, 177, 201);
            }
            QListWidget#list {
                border:1px solid #000;
                background-color:white;
                border-radius: 10px; 
                font-size:25px;                      
            }
            QPushButton#listdel{
                background-color: rgb(241,247,247); 
                border:1px solid #000; 
                border-radius: 10px;     
                font-size:25px;                                       
            }
            QPushButton#listadd{
                background-color: rgb(241,247,247); 
                border:1px solid #000; 
                border-radius: 10px;  
                font-size:25px;                                 
            }                   
        ''')
        self.list = QtWidgets.QListWidget(self.list_frame)
        self.list.setGeometry(QtCore.QRect(20, 20, 230, 310))
        self.list.setObjectName("list")
        self.listdel = QtWidgets.QPushButton(self.list_frame)
        self.listdel.setGeometry(QtCore.QRect(30, 340, 93, 31))
        self.listdel.setObjectName("listdel")
        self.listdel.clicked.connect(self.list_del_fn)
        self.listadd = QtWidgets.QPushButton(self.list_frame)
        self.listadd.setGeometry(QtCore.QRect(145, 340, 93, 31))
        self.listadd.setObjectName("listadd")
        self.listadd.clicked.connect(self.list_add_fn)


        self.homepage.raise_()
        self.loginpage.raise_()
        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        result=self.city_weather.query(firsttext,self.township.currentText())
        temperature_value, weather_description = result
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "魔鏡 Windows管家"))
        self.user_text.setText(_translate("Widget", "登入"))
        self.useradd_text.setText(_translate("Widget", "新增用戶"))
        self.home_text.setText(_translate("Widget", "首頁"))
        self.label_4.setText(_translate("Widget", "請輸入你用戶名稱:"))
        self.username.setText(_translate("Widget", "使用者名稱"))
        self.cpuname.setText(_translate("Widget", "CPU使用率(%):"))
        self.gpuname.setText(_translate("Widget", "GPU使用率(%):"))
        self.listdel.setText(_translate("Widget", "刪除"))
        self.listadd.setText(_translate("Widget", "新增"))
        self.temperature.setText(temperature_value)
        self.status.setText(weather_description)
        self.chatgpt_check_btn.setText("確認")
        

#------------以上都是介面---------
    #打開攝像頭
    def opencv(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while self.ocv:
            ret, frame = cap.read()
            self.frame=frame.copy()
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
    def account_num(self):
        self.name = None
    #用戶登入
    def userlogin(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.camera.setGeometry(QtCore.QRect(370, 100, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(930, 1000, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(930, 1000, 231, 31))
        self.Tick.setGeometry(QtCore.QRect(1160, 1000, 71, 61))
        #判斷是不是本人    
        ID=identify(self.frame)
        if bool(ID)==False :
            #顯示彈窗
            self.err()
        else :
            self.name=ID
            self.username.setText("歡迎%s進入" %ID)
            self.loginpage.setGeometry(QtCore.QRect(0, 1000, 1272, 721))
            self.homepage.setGeometry(QtCore.QRect(0, 0, 1272, 721))
            self.get_data_from_json()
            self.add_news()
            self.ocv=False
    #首頁
    def home(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 10, 600, 600))
        self.camera.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(930, 1000, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(930, 1000, 231, 31))
        self.Tick.setGeometry(QtCore.QRect(1160, 1000, 71, 61))
    #註冊用戶
    def add(self):
        self.graphicshome.setGeometry(QtCore.QRect(370, 1000, 512, 512))
        self.camera.setGeometry(QtCore.QRect(370, 100, 512, 512))
        self.lineEdit.setGeometry(QtCore.QRect(920, 190, 211, 61))
        self.label_4.setGeometry(QtCore.QRect(920, 140, 231, 31))
        self.Tick.setGeometry(QtCore.QRect(1160, 190, 71, 61))

    #check是打勾按鈕
    def check(self):
        if sign_up(self.lineEdit.text(),self.frame) == False :
            #顯示彈窗
            self.err()
        else :
            print("進入主畫面")
            mbox = QtWidgets.QMessageBox(Widget)
            mbox.setText("註冊成功，請登入")
            mbox.setIcon(2)
            mbox.exec()
    #顯示彈窗
    def err(self):
        mbox = QtWidgets.QMessageBox(Widget)
        mbox.setText("辨識失敗，請重試")
        mbox.setIcon(2)
        mbox.exec()

    #顯示CPU
    def update_cpu_usage(self,cpu_usage):
        self.cpu_usage_data.append(cpu_usage)
        if len(self.cpu_usage_data) > 50:
            self.cpu_usage_data.pop(0)
        self.ax_cpu.clear()
        self.ax_cpu.plot(self.cpu_usage_data, color='blue')
        self.ax_cpu.set_ylim([0,100])
        self.ax_cpu.set_xticks([])
        self.canvas_cpu.draw()
    #顯示GPU
    def update_gpu_usage(self,gpu_usage):
        self.gpu_usage_data.append(gpu_usage)
        if len(self.gpu_usage_data) > 50:
            self.gpu_usage_data.pop(0)
        self.ax_gpu.clear()
        self.ax_gpu.plot(self.gpu_usage_data, color='blue')
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

    def changetext(self):
        if join==1:
            result=self.city_weather.query(firsttext,self.township.currentText())
            temperature_value, weather_description = result
            self.temperature.setText(temperature_value) 
            if weather_description=="-99":
                weather_description=="多雲"
                pixmap = QtGui.QPixmap("image/weather/多雲.png")
                self.weatherimage.setPixmap(pixmap)
                self.status.setText("多雲")
            else :
                self.status.setText(weather_description)  
                # 使用QPixmap設定圖片的樣式
                if weather_description == "多雲":
                    pixmap = QtGui.QPixmap("image/weather/多雲.png")
                    self.weatherimage.setPixmap(pixmap)
                elif weather_description == "陰":
                    pixmap = QtGui.QPixmap("image/weather/陰.png")
                    self.weatherimage.setPixmap(pixmap)
                elif weather_description == "雨":
                    pixmap = QtGui.QPixmap("image/weather/雨.png")
                    self.weatherimage.setPixmap(pixmap)
                elif weather_description == "晴":
                    pixmap = QtGui.QPixmap("image/weather/晴.png")
                    self.weatherimage.setPixmap(pixmap)

    # slider 改變value
    def slider(self,value) :
        set_volume(value/100)
        self.volume_text.setText(f"{value}%")
        if value==0:
            self.volume.setStyleSheet(
            "background-image:url(\"image/volume-slash.png\")"
        )
        else:
            self.volume.setStyleSheet(
            "background-image:url(\"image/volume.png\")"
        )
    #代辦事項新增
    def list_add_fn(self):
        text,ok= QtWidgets.QInputDialog().getText(self.homepage, '新增事項', '請輸入新增的事項')
        add_district(self.name, text)
        self.list.addItem(text)
        self.get_data_from_json()
    #代辦事項刪除
    def list_del_fn(self):
        if self.list.currentIndex().row() !=-1:
            text=self.list.currentItem().text()
            print(self.list.currentItem().text())
            remove_value(self.name, text)
            self.list.takeItem(self.list.currentIndex().row())
            self.get_data_from_json()
        else:
            self.err()

    def get_data_from_json(self):
        try:
            with open('memorandum.json', 'r', encoding='utf-8') as f:
                load_dict = json.load(f)
            self.list.clear()
            for item in load_dict.get(self.name, []):
                self.list.addItem(item)
        except FileNotFoundError:
            print("JSON 文件不存在")
        except json.JSONDecodeError:
            print("JSON 解碼錯誤")
    #新增新聞
    def add_news(self):
        for i in range(20):
            self.newslist.addItem(self.line_news.news[i][0])
    #打開連結
    def open_link(self):
        # 定義超連結
        url = QUrl(self.line_news.news[self.newslist.currentIndex().row()][1])
        # 使用QDesktopServices打開超連結
        if not QDesktopServices.openUrl(url):
            # 如果無法打開超連結，可以在這裡處理錯誤
            errbox = QtWidgets.QMessageBox(self.homepage)
            errbox.setText("無法打開超連結")
            errbox.setIcon(2)
            errbox.exec()

    def weather_onEnter(self, event):
            #將QFrame內的所有子元件設定為hover狀態
            for child in self.weather.children():
                child.setStyleSheet('''
                    QLabel{
                        background-color:rgb(90,177,201);          
                    }
                ''')
            self.changetext    
    def weather_onLeave(self, event):
        #將QFrame內的所有子元件設定為正常狀態
        for child in self.weather.children():
            child.setStyleSheet('''
                QLabel{
                    background-color:rgb(239,245,245);          
                }
            ''')
        self.changetext
    def gpu_onEnter(self, event):
            for child in self.gpu.children():
                child.setStyleSheet('''
                    QLabel{
                        background-color:rgb(90,177,201);          
                    }
                ''')
    def gpu_onLeave(self, event):
        for child in self.gpu.children():
            child.setStyleSheet('''
                QLabel{
                    background-color:rgb(239,245,245);          
                }
            ''')
    def cpu_onEnter(self, event):
        for child in self.cpu.children():
            child.setStyleSheet('''
                QLabel{
                    background-color:rgb(90,177,201);          
                }
            ''')
    def cpu_onLeave(self, event):
        for child in self.cpu.children():
            child.setStyleSheet('''
                QLabel{
                    background-color:rgb(239,245,245);          
                }
            ''')
    def control_onEnter(self, event):
        for child in self.control.children():
            child.setStyleSheet('''
                QLabel{
                    background-color:rgb(90,177,201);          
                }
                QSlider{
                    background-color:rgb(90,177,201);                
                }
            ''')
    def control_onLeave(self, event):
        for child in self.control.children():
            child.setStyleSheet('''
                QLabel{
                    background-color:rgb(239,245,245);          
                }
                QSlider{
                    background-color:rgb(239,245,245);                
                }
            ''')
    def list_onEnter(self, event):
        for child in self.list_frame.children():
            child.setStyleSheet('''
                QPushButton{
                    background-color:rgb(90,177,201);          
                }
            ''')
    def list_onLeave(self, event):
        for child in self.list_frame.children():
            child.setStyleSheet('''
                QPushButton{
                    background-color:rgb(239,245,245);          
                }
            ''')
    
    #gpt回答
    def chatgpt_ans(self):
        ans=chatgpt(self.chatgpt_input.toPlainText())
        self.gpt.addItem(ans)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    ui.video_thread = threading.Thread(target=ui.opencv)
    ui.video_thread.start()
    sleep(3)
    Widget.show()
    sys.exit(app.exec_())
