from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
from .mini_card import MiniCard
from core.baseclass import CardBase, CardRiven, CardCommon
from .mini_card import MiniCard
import json

class EmptyCard(MiniCard):
    
    def __init__(self, index, parent=None):
        super().__init__(card=None, parent=parent)

        self.empty_pixmap_path = 'assets/ui/empty_frame.png'
        self.empty_background_pixmap = QPixmap(self.empty_pixmap_path)

        self.index = index

        self.selected_pixmap_path = 'assets/ui/select_frame.png'
        self.selected_background_pixmap = QPixmap(self.selected_pixmap_path)

        self.selected = False
        self.setVisible(True)

    def setSelected(self, selected: bool):
        """ 设置卡片的选中状态 """
        self.selected = selected
        self.update()

    def paintEvent(self, event):
        # 如果为空只绘制空背景，否则调用父类绘制后再绘制选中背景        
        self.cost_panel.setVisible(self.card is not None)
        if self.card is None:
            a_painter = QPainter(self)
            a_painter.begin(self)
            try:
                a_painter.setRenderHint(QPainter.Antialiasing)
                if not self.empty_background_pixmap.isNull():
                    a_painter.drawPixmap(self.rect(), self.empty_background_pixmap)
            finally:
                a_painter.end()
        else:
            super().paintEvent(event)
        if self.selected:
            b_painter = QPainter(self)
            b_painter.begin(self)
            try:
                b_painter.setRenderHint(QPainter.Antialiasing)
                if not self.selected_background_pixmap.isNull():
                    b_painter.drawPixmap(self.rect(), self.selected_background_pixmap)
            finally:
                b_painter.end()

    def setCard(self, card: CardBase | None):
        """ 设置卡片对象 """
        self.selected = False
        super().set_card(card)
        self.setVisible(True)
        self.update()

    def contextMenuEvent(self, event):
        if self.card is not None:
            self.setCard(None)
            if hasattr(self.parent().parent().parent(), 'RemoveCardFromBuild'):
                self.parent().parent().parent().RemoveCardFromBuild.emit(self)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if hasattr(self.parent().parent().parent(), 'SelectEmptyCard'):
                self.parent().parent().parent().SelectEmptyCard.emit(self)
        super().mousePressEvent(event)
