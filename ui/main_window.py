from qfluentwidgets import FluentWindow, SubtitleLabel, setFont, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QApplication
from .home_page import HomePage
from .card_gallery_page import CardGalleryPage


class MainWindow(FluentWindow):

    def __init__(self, context):
        super().__init__()
        self.context = context
        self.setObjectName('mainWindow')

        self.setWindowTitle('驱入虚空配卡工具')

        # create sub interface
        self.homeInterface = HomePage(self)
        self.cardGalleryInterface = CardGalleryPage(self.context, self)
        self.weaponBuildInterface = QFrame(self)
        self.rivenInterface = QFrame(self)
        self.settingInterface = QFrame(self)

        self.weaponBuildInterface.setObjectName('weaponBuildInterface')
        self.rivenInterface.setObjectName('rivenInterface')
        self.settingInterface.setObjectName('settingInterface')

        self.init_weapon_build_layout()
        self.init_riven_layout()
        self.init_setting_layout()

        self.initNavigation()
        self.initWindow()

    def init_home_layout(self):
        self.vBoxLayout = QVBoxLayout(self.homeInterface)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 20)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(SubtitleLabel('欢迎和帮助'))

    def init_weapon_build_layout(self):
        self.buildLayout = QVBoxLayout(self.weaponBuildInterface)
        self.buildLayout.setContentsMargins(36, 20, 36, 20)
        self.buildLayout.setSpacing(10)
        self.buildLayout.addWidget(SubtitleLabel('武器配卡'))

    def init_riven_layout(self):
        self.rivenLayout = QVBoxLayout(self.rivenInterface)
        self.rivenLayout.setContentsMargins(36, 20, 36, 20)
        self.rivenLayout.setSpacing(10)
        self.rivenLayout.addWidget(SubtitleLabel('自制紫卡'))

    def init_setting_layout(self):
        self.settingLayout = QVBoxLayout(self.settingInterface)
        self.settingLayout.setContentsMargins(36, 20, 36, 20)
        self.settingLayout.setSpacing(10)
        self.settingLayout.addWidget(SubtitleLabel('设置'))

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '欢迎和帮助')
        self.addSubInterface(self.weaponBuildInterface, FIF.DEVELOPER_TOOLS, '武器配卡')
        self.addSubInterface(self.rivenInterface, FIF.EDIT, '自制紫卡')
        self.addSubInterface(self.cardGalleryInterface, FIF.INFO, '卡牌一览')
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        w = QApplication.primaryScreen().availableGeometry().width()
        h = QApplication.primaryScreen().availableGeometry().height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def show(self):
        super().show()
        # Adjust font size based on screen scaling
        screen = self.screen()
        if screen:
            ratio = screen.devicePixelRatio()
            font = QApplication.font()
            # Set a base font size, e.g., 10, and scale it.
            # You might need to adjust the base size for your preference.
            font.setPointSize(int(10 * ratio))
            QApplication.setFont(font)
