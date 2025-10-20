from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QButtonGroup
from qfluentwidgets import ScrollArea, CheckBox, RadioButton, StrongBodyLabel
from core.baseclass import CardBase, CardRiven, CardCommon
from core.ivtenum import PropertyType, WeaponType
from .component.card_area import CardArea
from .component.flow_layout import FlowLayout
from .component.foldable_card_widget import FoldableCardWidget

class CardGalleryPage(QFrame):
    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.context = context
        self.setObjectName('cardGalleryPage')

        self.mainLayout = QVBoxLayout(self)

        # --- Filter Area ---
        # Weapon Type Filter
        self.weaponTypeFilterCard = FoldableCardWidget('武器类型', self)
        self.weaponTypeFilterWidget = QWidget(self.weaponTypeFilterCard)
        self.weaponTypeFilterFlowLayout = FlowLayout(self.weaponTypeFilterWidget, spacing=10)
        self.weaponTypeGroup = QButtonGroup(self)

        # Property Type Filter
        self.propertyTypeFilterCard = FoldableCardWidget('属性类型', self)
        self.propertyTypeFilterWidget = QWidget(self.propertyTypeFilterCard)
        self.propertyTypeFilterFlowLayout = FlowLayout(self.propertyTypeFilterWidget, spacing=10)
        self.propertyCheckboxes = {}

        # Card Type Filter
        self.cardTypeFilterCard = FoldableCardWidget('卡牌类型', self)
        self.cardTypeFilterWidget = QWidget(self.cardTypeFilterCard)
        self.cardTypeFilterFlowLayout = FlowLayout(self.cardTypeFilterWidget, spacing=10)
        self.cardTypeCheckboxes = {}

        # --- Card Area ---
        self.cardArea = CardArea(self.context, self)

        self._init_layout()
        self._init_weapon_type_filters()
        self._init_property_type_filters()
        self._init_card_type_filters()
        
        # Initial filter apply
        self._on_filter_changed()

    def _init_layout(self):
        """ Initialize the main layout and sub-layouts """
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)
        self.mainLayout.addWidget(self.weaponTypeFilterCard)
        self.mainLayout.addWidget(self.propertyTypeFilterCard)
        self.mainLayout.addWidget(self.cardTypeFilterCard)
        self.mainLayout.addWidget(self.cardArea, 1)
        
        # Layout for weapon type filter card
        self.weaponTypeFilterCard.contentLayout().addWidget(self.weaponTypeFilterWidget)

        # Layout for property type filter card
        self.propertyTypeFilterCard.contentLayout().addWidget(self.propertyTypeFilterWidget)

        # Layout for card type filter card
        self.cardTypeFilterCard.contentLayout().addWidget(self.cardTypeFilterWidget)

    def _init_weapon_type_filters(self):
        """ Create and add weapon type filter radio buttons """
        # Add 'All' option
        radio_all = RadioButton(str(WeaponType.All), self.weaponTypeFilterWidget)
        radio_all.setChecked(True)
        radio_all.setProperty('weaponType', WeaponType.All)
        radio_all.toggled.connect(self._on_filter_changed)
        self.weaponTypeFilterFlowLayout.addWidget(radio_all)
        self.weaponTypeGroup.addButton(radio_all)

        for weapon_type in WeaponType:
            if weapon_type == WeaponType.All:
                continue
            radio = RadioButton(str(weapon_type), self.weaponTypeFilterWidget)
            radio.setProperty('weaponType', weapon_type)
            radio.toggled.connect(self._on_filter_changed)
            self.weaponTypeFilterFlowLayout.addWidget(radio)
            self.weaponTypeGroup.addButton(radio)

    def _init_property_type_filters(self):
        """ Create and add property type filter checkboxes """
        for prop_type in PropertyType:
            if prop_type.name == '_Max':
                continue
            
            checkbox = CheckBox(str(prop_type), self)
            checkbox.stateChanged.connect(self._on_filter_changed)
            self.propertyTypeFilterFlowLayout.addWidget(checkbox)
            self.propertyCheckboxes[prop_type] = checkbox

    def _init_card_type_filters(self):
        """ Create and add card type filter checkboxes """
        card_types = {'紫卡': 'riven', 'Prime': 'prime', '普通': 'common'}
        for name, key in card_types.items():
            checkbox = CheckBox(name, self)
            checkbox.stateChanged.connect(self._on_filter_changed)
            self.cardTypeFilterFlowLayout.addWidget(checkbox)
            self.cardTypeCheckboxes[key] = checkbox

    def _on_filter_changed(self):
        """ Handle the filter change event by calling the card area's filter method. """
        # 1. Get selected weapon type
        selected_weapon_type = self.weaponTypeGroup.checkedButton().property('weaponType')

        # 2. Get selected property types
        selected_properties = {pt for pt, cb in self.propertyCheckboxes.items() if cb.isChecked()}
        
        # 3. Get selected card types
        selected_card_types = {key for key, cb in self.cardTypeCheckboxes.items() if cb.isChecked()}

        # 4. Apply filter to the card area
        self.cardArea.setFilter(selected_weapon_type, selected_properties, selected_card_types)

