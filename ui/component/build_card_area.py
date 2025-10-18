from .card_area import CardArea
from .selectable_mini_card import SelectableMiniCard
from core.baseclass import CardBase

class BuildCardArea(CardArea):
    """ 用于构筑的卡片区域 """
    def __init__(self, context, parent=None):
        super().__init__(context, parent)
        self.setObjectName('buildCardArea')

    def _create_card_widget(self, card: CardBase):
        """ Create a single Draggable MiniCard widget. """
        widget = SelectableMiniCard(card)
        # widget.setScale(0.5)
        return widget

    def _init_cards(self):
        """ Create and add all card widgets to the layout. """
        super()._init_cards()
        self.sort_cards()

    def setFilter(self, selected_weapon_type, selected_properties, selected_card_types):
        """
        Filters the displayed cards based on the provided criteria.
        """
        super().setFilter(selected_weapon_type, selected_properties, selected_card_types)
        self.sort_cards()

    def sort_cards(self):
        """ Sorts the cards in the layout based on their priority. """
        widgets = [self.cardLayout.itemAt(i).widget() for i in range(self.cardLayout.count())]
        
        # Sort widgets by priority (descending)
        widgets.sort(key=lambda w: w.priority, reverse=True)
        
        # Re-add widgets to the layout in sorted order
        for widget in widgets:
            self.cardLayout.addWidget(widget)

    def getCardWidgetByCard(self, card: CardBase) -> SelectableMiniCard | None:
        """ 根据卡片对象获取对应的卡片组件 """
        for i in range(self.cardLayout.count()):
            widget = self.cardLayout.itemAt(i).widget()
            if isinstance(widget, SelectableMiniCard) and widget.card == card:
                return widget
        return None
    
    def getAvailableCards(self) -> list[CardBase]:
        """ 获取当前区域内所有可用的卡片对象列表 """
        cards = []
        for i in range(self.cardLayout.count()):
            widget = self.cardLayout.itemAt(i).widget()
            if isinstance(widget, SelectableMiniCard) and widget.card is not None:
                cards.append(widget.card)
        return cards