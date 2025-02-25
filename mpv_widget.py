from PyQt6.QtWidgets import QWidget, QVBoxLayout
import mpv


class MpvWidget(QWidget):
    def __init__(self, parent=None):
        import locale

        locale.setlocale(locale.LC_NUMERIC, "C")
        QWidget.__init__(self, parent)
        # 创建一个垂直布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建 MPV 播放器实例
        self.mpv = mpv.MPV(
            wid=str(int(self.winId())), log_handler=print, loglevel="debug"
        )

        # 设置一些基本的 MPV 属性
        self.mpv.keep_open = True  # 播放结束后保持打开状态
        self.mpv.osd_level = 0  # 不显示 MPV 自带的 OSD

        # 设置视频播放的一些属性
        self.mpv.hwdec = "auto"  # 启用硬件解码

    def closeEvent(self, event):
        self.mpv.terminate()
        super().closeEvent(event)

    def play_pause(self):
        self.mpv.pause = not self.mpv.pause

    def get_duration(self):
        # 获取视频总时长（秒）
        try:
            return self.mpv.duration
        except:
            return 0

    def get_time_pos(self):
        # 获取当前播放位置（秒）
        try:
            return self.mpv.time_pos
        except:
            return 0

    def seek(self, position):
        # 跳转到指定位置（秒）
        self.mpv.seek(position, "absolute")

    def set_volume(self, volume):
        # 设置音量（0-100）
        self.mpv.volume = volume
