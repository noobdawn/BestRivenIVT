from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor
from PyQt5.QtCore import Qt
from core.baseclass import CardBase, CardRiven, CardCommon
from core.ivtenum import SlotToString

class CostPanel(QWidget):
    """A widget that draws a pixmap as its background."""
    def __init__(self, pixmap_path, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(pixmap_path)
        self.setFixedSize(66, 25)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.pixmap.isNull():
            painter.drawPixmap(self.rect(), self.pixmap)
        super().paintEvent(event)

class MiniCard(QWidget):
    """
    一个小组件，用于以小图的形式展示卡牌的cost和名称。
    背景图片来自于 assets/ui/frame开头。
    """
    def __init__(self, card: CardBase = None, parent=None):
        super().__init__(parent)
        self.card = card
        # 如果是CardCommon，则使用普通卡牌背景
        if isinstance(card, CardCommon):
            if card.isPrime:
                self.background_pixmap = QPixmap('assets/ui/frame_prime.png')
            else:
                self.background_pixmap = QPixmap('assets/ui/frame_gold.png')
        else:
            self.background_pixmap = QPixmap('assets/ui/frame_riven.png')

        self.setFixedSize(124, 128)

        self.cost_panel = CostPanel('assets/ui/costpanel.png', self)
        self.slot_label = QLabel(self.cost_panel)
        self.cost_label = QLabel(self.cost_panel)
        self.name_label = QLabel(self)

        self._setup_ui()
        self.set_card(card)

    def _setup_ui(self):
        """初始化UI元素和布局。"""
        cost_layout = QHBoxLayout(self.cost_panel)
        cost_layout.setContentsMargins(0, 0, 0, 0)
        cost_layout.setSpacing(0)

        # slot label
        self.slot_label.setFixedSize(30, 30)
        self.slot_label.setScaledContents(True)
        cost_layout.addWidget(self.slot_label)

        # 配置 Cost 标签
        font_cost = QFont()
        font_cost.setBold(True)
        font_cost.setPointSize(11)
        self.cost_label.setFont(font_cost)
        self.cost_label.setAlignment(Qt.AlignCenter)
        self.cost_label.setStyleSheet("color: white; background-color: transparent;")
        cost_layout.addWidget(self.cost_label)

        # 配置 Name 标签
        font_name = QFont()
        font_name.setPointSize(9)
        self.name_label.setFont(font_name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("color: white; background-color: transparent;")

        # 使用布局来定位标签
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.cost_panel, 0, Qt.AlignTop | Qt.AlignHCenter)
        layout.addStretch()
        layout.addWidget(self.name_label)
        layout.addStretch()
        self.setLayout(layout)

    def set_card(self, card: CardBase):
        """设置要显示的卡牌。如果卡牌为None，则隐藏该组件。"""
        self.card = card
        if self.card:
            self.cost_label.setText(str(self.card.cost))
            if self.card.slot is not None and self.card.slot in SlotToString:
                slot_image_path = f"assets/ui/{SlotToString[self.card.slot]}.png"
                slot_image = QPixmap(slot_image_path)
                self.slot_label.setPixmap(slot_image)
                self.slot_label.setVisible(True)
                slot_size = slot_image.size()
                self.slot_label.setFixedHeight(20)
                self.slot_label.setFixedWidth(20 * slot_size.width() // slot_size.height())
            else:
                self.slot_label.setVisible(False)

            self.name_label.setText(self.card.name)
            self.setToolTip(f"{self.card.name}\nCost: {self.card.cost}")
            self.setVisible(True)
        else:
            self.cost_label.setText("")
            self.name_label.setText("")
            self.slot_label.clear()
            self.setVisible(False)

    def paintEvent(self, event):
        """绘制背景图片或默认背景。"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.background_pixmap.isNull():
            # 绘制背景图，保持比例并填充
            painter.drawPixmap(self.rect(), self.background_pixmap)
        else:
            # 如果图片不存在，绘制一个深灰色矩形作为备用背景
            painter.fillRect(self.rect(), QColor(45, 45, 45))
        
        # 调用父类的paintEvent来确保子控件（QLabel）被正确绘制
        super().paintEvent(event)
