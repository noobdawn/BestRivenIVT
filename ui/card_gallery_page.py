from PyQt5.QtWidgets import QFrame
from qfluentwidgets import ScrollArea
from core.baseclass import CardBase
from ui.component.mini_card import MiniCard
from .component.flow_layout import FlowLayout

class CardGalleryPage(ScrollArea):
    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.context = context
        self.setObjectName('cardGalleryPage')
        self.view = QFrame(self)
        self.flowLayout = FlowLayout(self.view)

        self._init_layout()
        self._init_cards()

        self.setWidget(self.view)
        self.setWidgetResizable(True)

    def _init_layout(self):
        self.flowLayout.setContentsMargins(36, 20, 36, 20)
        self.flowLayout.setSpacing(0)

    def _init_cards(self):
        all_cards = self.context.all_cards
        for card in all_cards:
            card_widget = self._create_card_widget(card)
            self.flowLayout.addWidget(card_widget)

    def _create_card_widget(self, card : CardBase):
        widget = MiniCard(card)
        return widget
