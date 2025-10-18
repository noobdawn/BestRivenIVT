from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtCore import Qt
from .mini_card import MiniCard
from core.baseclass import CardBase
import json

FONT_SIZE = 12

class SelectableMiniCard(MiniCard):
    """
    一个可选择的MiniCard组件，支持拖放操作。
    """
    def __init__(self, card: CardBase = None, parent=None):
        super().__init__(card, parent)
        self.index = -1 # -1表示未被装备，0~7代表装备槽位
        self.priority = 0 # 优先级，数值越大优先级越高
        
    def paintEvent(self, event):
        super().paintEvent(event)
        # 额外绘制priority
        painter = QPainter(self)
        painter.begin(self)
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            font = QFont()
            font.setPointSize(FONT_SIZE)
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(Qt.yellow)
            # 画在卡片正中央
            priority_text = f"{self.priority:.2f}%"
            if self.priority > 0:
                painter.drawText(self.rect(), Qt.AlignCenter, priority_text)
        finally:
            painter.end()

    def setSelected(self, selected_slot: int):
        """ 设置卡片的选中状态 """
        self.index = selected_slot
        if selected_slot == -1:
            self.name_label.setText(self.card.name)
        else:
            self.name_label.setText(f"{self.card.name}[{selected_slot}]")

    def setPriority(self, priority: int):
        """ 设置卡片的优先级 """
        self.priority = priority
        self.update()

    def contextMenuEvent(self, event):
        return  # 禁用右键菜单
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.card is not None:
            weaponBuildPage = self.parent().parent().parent().parent().parent().parent().parent().parent()
            if hasattr(weaponBuildPage, 'OnCardSelected'):
                weaponBuildPage.OnCardSelected.emit(self.card)
        super().mousePressEvent(event)