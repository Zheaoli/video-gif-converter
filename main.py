import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
import vendor.mpv as mpv


class MpvWidget(QWidget):
    def __init__(self, parent=None):
        import locale
        locale.setlocale(locale.LC_ALL, 'C')
        super().__init__(parent)
        # 创建一个垂直布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建 MPV 播放器实例
        self.mpv = mpv.MPV(
            wid=str(int(self.winId())),
            log_handler=print,
            loglevel='debug'
        )
        
        # 设置一些基本的 MPV 属性
        self.mpv.loop = 'inf'
        self.mpv.keep_open = True
        
    def closeEvent(self, event):
        self.mpv.terminate()
        super().closeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MPV Video Player")
        self.resize(800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        
        self.mpv_widget = MpvWidget(self)
        layout.addWidget(self.mpv_widget)
        
        self.load_video()
    
    def load_video(self):
        # 这里可以替换为实际的视频文件路径
        video_path = "/home/manjusaka/Documents/Laid-Back Camp - S01E01 - Mount Fuji and Curry Noodles HDTV-1080p.mkv"
        try:
            self.mpv_widget.mpv.play(video_path)
        except Exception as e:
            print(f"Error loading video: {e}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()