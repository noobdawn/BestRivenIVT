import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from core.context import APP_CONTEXT

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # Enable high DPI scaling

def main():
    # 在创建UI之前加载所有数据
    APP_CONTEXT.load_data()

    app = QApplication(sys.argv)

    # 创建主窗口并传入应用上下文
    main_win = MainWindow(APP_CONTEXT)

    # 显示主窗口
    main_win.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()

