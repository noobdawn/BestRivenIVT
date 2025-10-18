from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap

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