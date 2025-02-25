from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,QFileDialog
from qfluentwidgets import (Slider, ToggleToolButton, FluentIcon, InfoBar,
                           InfoBarPosition,TransparentToolButton )
import os
from mpv_widget import MpvWidget

class VideoPlayerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # 顶部工具栏布局
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        
        # 添加打开文件按钮
        self.open_file_btn = TransparentToolButton(FluentIcon.FOLDER_ADD, self)
        self.open_file_btn.setToolTip("打开视频文件")
        self.open_file_btn.clicked.connect(self.open_file_dialog)
        toolbar_layout.addWidget(self.open_file_btn)
        toolbar_layout.addStretch(1)  # 占据剩余空间
        
        # 创建播放器区域
        self.player_frame = QFrame()
        self.player_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.player_frame.setStyleSheet("background-color: black;")
        player_layout = QVBoxLayout(self.player_frame)
        player_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建 MPV 播放器
        self.mpv_widget = MpvWidget(self)
        player_layout.addWidget(self.mpv_widget)
        
        # 控制条布局
        control_layout = QVBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(5)
        
        # 进度条和时间显示的布局
        progress_layout = QHBoxLayout()
        
        # 添加当前时间标签
        self.current_time_label = QLabel("00:00:00")
        self.current_time_label.setStyleSheet("color: #FFFFFF;")
        self.current_time_label.setFixedWidth(70)
        self.current_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        # 进度条
        self.progress_slider = Slider(Qt.Orientation.Horizontal, self)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.setValue(0)
        self.progress_slider.sliderReleased.connect(self.seek_position)
        self.progress_slider.mouseReleaseEvent = lambda event: self.seek_position()
        
        # 总时长标签
        self.total_time_label = QLabel("00:00:00")
        self.total_time_label.setStyleSheet("color: #FFFFFF;")
        self.total_time_label.setFixedWidth(70)
        self.total_time_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # 添加到进度布局
        progress_layout.addWidget(self.current_time_label)
        progress_layout.addWidget(self.progress_slider, 1)  # 进度条占据剩余空间
        progress_layout.addWidget(self.total_time_label)
        
        # 播放控制按钮布局
        playback_layout = QHBoxLayout()
        
        # 播放/暂停按钮
        self.play_pause_btn = ToggleToolButton(FluentIcon.PLAY, self)
        self.play_pause_btn.setFixedSize(QSize(36, 36))
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        
        # 音量控制
        self.volume_button = ToggleToolButton(FluentIcon.VOLUME, self)
        self.volume_button.setFixedSize(QSize(36, 36))
        self.volume_button.clicked.connect(self.toggle_mute)
        
        # 音量滑块
        self.volume_slider = Slider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.volume_slider.setFixedWidth(100)
        
        # 添加控制元素到布局
        playback_layout.addWidget(self.play_pause_btn)
        playback_layout.addStretch(1)  # 在播放按钮和音量控制之间添加弹性空间
        playback_layout.addWidget(self.volume_button)
        playback_layout.addWidget(self.volume_slider)
        
        # 将组件添加到控制布局
        control_layout.addLayout(progress_layout)
        control_layout.addLayout(playback_layout)
        
        # 将组件添加到主布局
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.player_frame, 1)  # 播放器区域占据剩余空间
        main_layout.addLayout(control_layout)
        
        # 初始化视频路径
        self.video_path = None
        
        # 创建定时器来更新进度
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(200)  # 200毫秒更新一次
        self.update_timer.timeout.connect(self.update_progress)
        self.update_timer.start()
        
        # 设置进度条样式
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #404040;
                margin: 0px;
                border-radius: 2px;
            }
            
            QSlider::handle:horizontal {
                background: #0078D4;
                border: none;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            
            QSlider::sub-page:horizontal {
                background: #0078D4;
                border-radius: 2px;
            }
        """)
    
    def open_file_dialog(self):
        """打开文件选择对话框"""
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("选择视频文件")
        file_dialog.setNameFilter("视频文件 (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm *.m4v *.mpg *.mpeg *.3gp *.ogv);;所有文件 (*.*)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.load_video(selected_files[0])
        
    def format_time(self, seconds):
        """将秒数转换为 HH:MM:SS 格式"""
        if seconds is None:
            return "00:00:00"
        
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        
        return f"{h:02}:{m:02}:{s:02}"
        
    def update_progress(self):
        """更新进度条和时间显示"""
        if not self.video_path:
            return
            
        try:
            duration = self.mpv_widget.get_duration()
            current_position = self.mpv_widget.get_time_pos()
            
            if duration and current_position is not None:
                # 更新进度条，避免触发 sliderReleased 信号
                self.progress_slider.blockSignals(True)
                self.progress_slider.setValue(int(current_position / duration * 1000))
                self.progress_slider.blockSignals(False)
                
                # 更新时间标签
                self.current_time_label.setText(self.format_time(current_position))
                self.total_time_label.setText(self.format_time(duration))
        except Exception as e:
            print(f"更新进度时出错: {e}")
    
    def load_video(self, path):
        if not os.path.exists(path):
            InfoBar.error(
                title="错误",
                content=f"视频文件不存在: {path}",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return
        
        # 如果之前有播放的视频，先停止
        if self.video_path:
            try:
                self.mpv_widget.mpv.stop()
            except:
                pass
            
        # 重置进度条和时间显示
        self.progress_slider.blockSignals(True)
        self.progress_slider.setValue(0)
        self.progress_slider.blockSignals(False)
        self.current_time_label.setText("00:00:00")
        self.total_time_label.setText("00:00:00")
            
        self.video_path = path
        try:
            self.mpv_widget.mpv.play(path)
            self.mpv_widget.mpv.pause = False  # 加载后自动播放
            self.play_pause_btn.setChecked(True)  # 更新按钮状态
            
            # 显示成功通知
            InfoBar.success(
                title="成功",
                content=f"视频已加载: {os.path.basename(path)}",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=2000
            )
        except Exception as e:
            InfoBar.error(
                title="播放错误",
                content=str(e),
                parent=self,
                position=InfoBarPosition.TOP
            )
    
    def toggle_play_pause(self):
        if self.video_path:
            self.mpv_widget.play_pause()
    
    def seek_position(self):
        if self.video_path:
            duration = self.mpv_widget.get_duration()
            if duration:
                position = self.progress_slider.value() / 1000 * duration
                self.mpv_widget.seek(position)
    
    def toggle_mute(self):
        if hasattr(self.mpv_widget.mpv, 'mute'):
            self.mpv_widget.mpv.mute = not self.mpv_widget.mpv.mute
    
    def set_volume(self, volume):
        if self.video_path:
            self.mpv_widget.set_volume(volume)