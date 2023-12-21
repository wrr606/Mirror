import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import psutil
from matplotlib import pyplot as plt

class CPUMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        plt.rcParams["font.sans-serif"]="Microsoft JhengHei"
        plt.rcParams["axes.unicode_minus"]=False
        self.setWindowTitle("CPU 使用率監測器")
        self.setGeometry(100, 100, 400, 200)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.cpu_usage_data = [0] * 50  # 初始化 50 筆數據，初始值為 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cpu_usage)
        self.timer.start(1000)  # 更新間隔：1000 毫秒（1 秒）

    def update_cpu_usage(self):
        cpu_usage = min(psutil.cpu_percent(interval=0.1), 100)  # 將使用率上限設定為 100
        self.cpu_usage_data.append(cpu_usage)

        # 限制顯示最近的 50 筆數據
        if len(self.cpu_usage_data) > 50:
            self.cpu_usage_data.pop(0)

        # 顯示最近的 50 筆數據
        self.ax.clear()
        self.ax.bar(range(len(self.cpu_usage_data)), self.cpu_usage_data, color='blue')
        self.ax.set_ylim([0, 100])  # 設定 y 軸範圍為 0 到 100
        self.ax.set_ylabel('使用率 (%)')
        self.ax.set_xticks([])  # 不顯示 x 軸刻度
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor_app = CPUMonitorApp()
    monitor_app.show()
    sys.exit(app.exec_())
