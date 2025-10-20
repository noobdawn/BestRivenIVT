from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMenu, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from core.baseclass import CardBase, CardRiven, CardCommon
from core.ivtenum import SlotToString
from data.cards import delete_riven_card
from core.context import APP_CONTEXT
from .cost_panel import CostPanel

FONT_SIZE = 12

class MiniCard(QWidget):
    """
    一个小组件，用于以小图的形式展示卡牌的cost和名称。
    背景图片来自于 assets/ui/frame开头。
    """

    def __init__(self, card: CardBase = None, parent=None):
        super().__init__(parent)
        self.card = card
        self.base_pixmap_path = self._get_pixel_map_path()
        self.base_pixmap = QPixmap(self.base_pixmap_path)
        self.is_active = True

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
        font_cost.setPointSize(12)
        self.cost_label.setFont(font_cost)
        self.cost_label.setAlignment(Qt.AlignCenter)
        cost_layout.addWidget(self.cost_label)

        # 配置 Name 标签
        font_name = QFont()
        font_name.setPointSize(FONT_SIZE)
        self.name_label.setFont(font_name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)

        # 使用布局来定位标签
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(5, 5, 5, 5)
        self.card_layout.addWidget(self.cost_panel, 0, Qt.AlignTop | Qt.AlignHCenter)
        self.card_layout.addStretch()
        self.card_layout.addWidget(self.name_label)
        self.card_layout.addStretch()
        self.setLayout(self.card_layout)
        
        self.setActive(True) # Set initial active state

    def set_card(self, card: CardBase):
        """设置要显示的卡牌。如果卡牌为None，则隐藏该组件。"""
        self.card = card      
        # 存储原始图片路径
        self.base_pixmap_path = self._get_pixel_map_path()
        self.base_pixmap = QPixmap(self.base_pixmap_path)

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
            # Build tooltip from properties
            prop_texts = [str(prop) for prop in self.card.properties]
            tooltip_text = "\n".join(prop_texts)
            self.setToolTip(tooltip_text)
            self.setVisible(True)
        else:
            self.cost_label.setText("")
            self.name_label.setText("")
            self.slot_label.clear()
            self.setVisible(False)

    def setActive(self, active: bool):
        """设置卡片的激活状态，影响UI显示。"""
        self.is_active = active
        if active:
            self.background_pixmap = QPixmap(self.base_pixmap_path)
            self.name_label.setStyleSheet("color: white; background-color: transparent;")
            self.cost_label.setStyleSheet("color: white; background-color: transparent;")
        else:
            gray_pixmap_path = self.base_pixmap_path.replace('.png', '_gray.png')
            self.background_pixmap = QPixmap(gray_pixmap_path)
            self.name_label.setStyleSheet("color: gray; background-color: transparent;")
            self.cost_label.setStyleSheet("color: gray; background-color: transparent;")
        self.update()  # Trigger a repaint

    def setScale(self, scale: float):
        """设置整个组件的缩放比例。"""
        # 更新组件大小
        self.setFixedSize(int(124 * scale), int(128 * scale))
        self.cost_panel.setFixedSize(int(66 * scale), int(25 * scale))

        # 更新字体大小
        font_cost = self.cost_label.font()
        font_cost.setPointSize(int(12 * scale))
        self.cost_label.setFont(font_cost)

        font_name = self.name_label.font()
        font_name.setPointSize(int(FONT_SIZE * scale))
        self.name_label.setFont(font_name)

        # 更新极性图标大小
        if self.card and self.card.slot is not None and self.card.slot in SlotToString:
            slot_image_path = f"assets/ui/{SlotToString[self.card.slot]}.png"
            slot_image = QPixmap(slot_image_path)
            if not slot_image.isNull():
                slot_size = slot_image.size()
                new_height = int(20 * scale)
                new_width = int(new_height * slot_size.width() / slot_size.height())
                self.slot_label.setFixedHeight(new_height)
                self.slot_label.setFixedWidth(new_width)

    def paintEvent(self, event):
        """绘制背景图片或默认背景。"""
        painter = QPainter()
        painter.begin(self)
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            
            if not self.background_pixmap.isNull():
                # 绘制背景图，保持比例并填充
                painter.drawPixmap(self.rect(), self.background_pixmap)
            else:
                # 如果图片不存在，绘制一个深灰色矩形作为备用背景
                painter.fillRect(self.rect(), QColor(45, 45, 45))
        finally:
            painter.end()
        
        # 调用父类的paintEvent来确保子控件（QLabel）被正确绘制
        super().paintEvent(event)

    def contextMenuEvent(self, event):
        if isinstance(self.card, CardRiven):
            menu = QMenu(self)
            delete_action = menu.addAction("删除")
            action = menu.exec_(self.mapToGlobal(event.pos()))

            if action == delete_action:
                self._handle_delete()

    def _handle_delete(self):
        reply = QMessageBox.question(self, '确认删除', 
                                     f'你确定要删除这张自定义紫卡 "{self.card.name}" 吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if delete_riven_card(self.card.name):
                # Reload data and notify
                APP_CONTEXT.load_data()
                APP_CONTEXT.card_data_changed.emit()
            else:
                QMessageBox.warning(self, '删除失败', '删除紫卡时发生错误。')

    def _get_pixel_map_path(self) -> str:
        """获取当前卡片的背景图片路径。"""
        if isinstance(self.card, CardCommon):
            if self.card.isPrime:
                return 'assets/ui/frame_prime.png'
            else:
                return 'assets/ui/frame_gold.png'
        else:
            return 'assets/ui/frame_riven.png'