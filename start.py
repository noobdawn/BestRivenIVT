import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ui.main_window import MainWindow
from core.context import APP_CONTEXT 

# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # Enable high DPI scaling

def main():
    # 在创建UI之前加载所有数据
    APP_CONTEXT.load_data()

    app = QApplication(sys.argv)

    # 创建启动页
    splash_pix = QPixmap('assets/images/Splash.jpg')
    splash = QSplashScreen(splash_pix)
    splash.showMessage('正在启动应用程序...', Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    splash.show()

    # 创建主窗口并传入应用上下文
    main_win = MainWindow(APP_CONTEXT)

    # 隐藏启动页并显示主窗口
    splash.finish(main_win)
    main_win.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()