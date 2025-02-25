import os

# 导入 PyQt-Fluent-Widgets 组件
from qfluentwidgets import (
    FluentWindow,
    setThemeColor,
    Theme,
    setTheme,
    InfoBar,
    InfoBarPosition,
)

# 设置资源路径
from video_player import VideoPlayerWidget


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluent MPV Video Player")
        self.resize(900, 600)

        # 设置主题颜色
        setThemeColor("#0078d4")  # 使用蓝色主题
        setTheme(Theme.AUTO)  # 自动跟随系统主题

        # 创建视频播放器部件
        self.video_player = VideoPlayerWidget(self)

        # 将播放器添加到堆叠部件
        self.stackedWidget.addWidget(self.video_player)
        self.stackedWidget.setCurrentWidget(self.video_player)

        # 移除导航界面，改用单一界面模式
        self.navigationInterface.setVisible(False)
