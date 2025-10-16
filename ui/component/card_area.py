from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ScrollArea, CardWidget, TitleLabel
from core.baseclass import CardBase, CardRiven, CardCommon
from core.ivtenum import WeaponType
from .mini_card import MiniCard
from .flow_layout import FlowLayout

class CardArea(QWidget):
    """ A widget that displays a collection of cards with filtering capabilities. """

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.context = context
        self.setObjectName('cardArea')
        self.objectName

        self.mainLayout = QVBoxLayout(self)
        self.cardsCard = CardWidget(self)
        self.cardsCardLayout = QVBoxLayout(self.cardsCard)
        self.cardsTitle = TitleLabel('卡牌', self.cardsCard)
        self.scrollArea = ScrollArea(self.cardsCard)
        self.cardView = QWidget(self.scrollArea)
        self.cardLayout = FlowLayout(self.cardView)

        self._init_layout()
        self._init_cards()
        self.context.card_data_changed.connect(self.refresh)

    def refresh(self):
        """ Refresh the card display based on the current filter. """
        for i in reversed(range(self.cardLayout.count())):
            widget = self.cardLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self._init_cards()
        # This assumes that the filter state is stored in the context.
        selected_weapon_type = getattr(self.context, 'selected_weapon_type', WeaponType.All)
        selected_properties = getattr(self.context, 'selected_properties', set())
        selected_card_types = getattr(self.context, 'selected_card_types', set())
        self.setFilter(selected_weapon_type, selected_properties, selected_card_types)
        # clear all widgets

    def _init_layout(self):
        """ Initialize the layout. """
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.cardsCard)

        self.cardsCardLayout.setContentsMargins(10, 10, 10, 10)
        self.cardsCardLayout.addWidget(self.cardsTitle)
        self.cardsCardLayout.addWidget(self.scrollArea)
        self.scrollArea.setWidget(self.cardView)
        self.scrollArea.setWidgetResizable(True)
        
        self.cardLayout.setContentsMargins(0, 0, 0, 0)
        self.cardLayout.setSpacing(4)

    def _init_cards(self):
        """ Create and add all card widgets to the layout. """
        all_cards = self.context.all_cards
        for card in all_cards:
            card_widget = self._create_card_widget(card)
            self.cardLayout.addWidget(card_widget)

    def setFilter(self, selected_weapon_type, selected_properties, selected_card_types):
        """
        Filters the displayed cards based on the provided criteria.
        """
        all_widgets = [self.cardLayout.itemAt(i).widget() for i in range(self.cardLayout.count())]
        
        # If no filters are selected at all, show all cards
        if not selected_weapon_type and not selected_properties and not selected_card_types:
            for widget in all_widgets:
                widget.show()
            # Restore original order
            for widget in sorted(all_widgets, key=lambda w: w.card.name):
                self.cardLayout.addWidget(widget)
            return

        matched_widgets = []
        unmatched_widgets = []

        for widget in all_widgets:
            card = widget.card
            
            # Check weapon type
            weapon_match = (
                not selected_weapon_type or
                selected_weapon_type == WeaponType.All
                or (isinstance(card, CardBase) and card.weaponType == selected_weapon_type)
            )

            # Check card type
            card_type_match = not selected_card_types
            if not card_type_match:
                if 'riven' in selected_card_types and isinstance(card, CardRiven):
                    card_type_match = True
                elif 'prime' in selected_card_types and isinstance(card, CardCommon) and card.isPrime:
                    card_type_match = True
                elif 'common' in selected_card_types and isinstance(card, CardCommon) and not card.isPrime:
                    card_type_match = True

            # Check properties
            prop_match = not selected_properties
            if not prop_match:
                card_properties = {prop.propertyType for prop in card.properties}
                if selected_properties.intersection(card_properties):
                    prop_match = True

            # Final decision
            if weapon_match and card_type_match and prop_match:
                widget.show()
                matched_widgets.append(widget)
            else:
                widget.hide()
                unmatched_widgets.append(widget)
        
        # Re-add widgets to the layout to bring matched items to the front
        for widget in matched_widgets:
            self.cardLayout.addWidget(widget)
        
        for widget in unmatched_widgets:
            self.cardLayout.addWidget(widget)

        # 更新context
        self.context.selected_weapon_type = selected_weapon_type
        self.context.selected_properties = selected_properties
        self.context.selected_card_types = selected_card_types

    def _create_card_widget(self, card: CardBase):
        """ Create a single MiniCard widget. """
        widget = MiniCard(card)
        widget.setScale(0.5)
        return widget
