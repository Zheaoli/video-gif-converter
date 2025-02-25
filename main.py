import sys
from PyQt6.QtWidgets import QApplication

# 导入 PyQt-Fluent-Widgets 组件

# 设置资源路径
from qfluentwidgets import FluentTranslator
from main_window import MainWindow



def main():
    # 创建应用
    app = QApplication(sys.argv)

    # 添加翻译器
    translator = FluentTranslator()
    app.installTranslator(translator)

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
