from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget
from qfluentwidgets import (CardWidget, TitleLabel, LineEdit, ComboBox, 
                            PushButton, TransparentToolButton, FluentIcon as FIF, StrongBodyLabel,
                            BodyLabel, FlowLayout, InfoBar, InfoBarPosition)
import json
import os

from core.ivtenum import (PropertyType, SlotToText, Slot, WeaponType, WeaponTypeToString,
                           RivenRange, RivenRangeToString, calculate_riven_property_range)
from core.baseclass import CardRiven, Property
from data.cards import save_riven_card, get_card_by_name
from .component.card_area import CardArea
from .component.value_edit import ValueEdit

class PropertyEditor(QWidget):
    """Widget for editing a single property."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.property_type_combo = ComboBox(self)
        self.property_value_edit = ValueEdit(input_type='float', is_percentage=True, parent=self)
        self.remove_button = TransparentToolButton(FIF.REMOVE, self)

        self.layout.addWidget(StrongBodyLabel("属性:", self))
        self.layout.addWidget(self.property_type_combo, 1)
        self.layout.addWidget(StrongBodyLabel("数值:", self))
        self.layout.addWidget(self.property_value_edit, 1)
        self.layout.addWidget(self.remove_button)

        self._init_property_types()

    def _init_property_types(self):
        for prop_type in PropertyType:
            if prop_type.name != '_Max':
                self.property_type_combo.addItem(prop_type.toString(), userData=prop_type)

class RivenPage(QFrame):
    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.context = context
        self.setObjectName('rivenPage')
        self.property_editors = []

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

        # Card 1: Basic Info
        self.basicInfoCard = CardWidget(self)
        self.basicInfoLayout = QVBoxLayout(self.basicInfoCard)
        self.basicInfoTitle = TitleLabel('基础信息', self.basicInfoCard)
        
        self.name_layout = QHBoxLayout()
        self.name_label = StrongBodyLabel('卡牌名称:', self)
        self.name_edit = LineEdit(self)
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_edit)

        self.slot_layout = QHBoxLayout()
        self.slot_label = StrongBodyLabel('极性:', self)
        self.slot_combo = ComboBox(self)
        self.slot_layout.addWidget(self.slot_label)
        self.slot_layout.addWidget(self.slot_combo)

        self.weapon_type_layout = QHBoxLayout()
        self.weapon_type_label = StrongBodyLabel('武器类型:', self)
        self.weapon_type_combo = ComboBox(self)
        self.weapon_type_layout.addWidget(self.weapon_type_label)
        self.weapon_type_layout.addWidget(self.weapon_type_combo)

        self.riven_range_layout = QHBoxLayout()
        self.riven_range_label = StrongBodyLabel('正负增益数量:', self)
        self.riven_range_combo = ComboBox(self)
        self.riven_range_layout.addWidget(self.riven_range_label)
        self.riven_range_layout.addWidget(self.riven_range_combo)

        self.basicInfoLayout.addWidget(self.basicInfoTitle)
        self.basicInfoLayout.addLayout(self.name_layout)
        self.basicInfoLayout.addLayout(self.slot_layout)
        self.basicInfoLayout.addLayout(self.weapon_type_layout)
        self.basicInfoLayout.addLayout(self.riven_range_layout)

        self.saveButton = PushButton(FIF.SAVE, '保存', self)
        self.basicInfoLayout.addWidget(self.saveButton, 0, Qt.AlignRight)

        # Card 2: Properties
        self.propertiesCard = CardWidget(self)
        self.propertiesLayout = QVBoxLayout(self.propertiesCard)
        self.propertiesTitle = TitleLabel('属性', self.propertiesCard)
        self.addPropertyButton = PushButton(FIF.ADD, '添加属性', self)
        self.propertiesListLayout = QVBoxLayout()

        self.propertiesLayout.addWidget(self.propertiesTitle)
        self.propertiesLayout.addLayout(self.propertiesListLayout)
        self.propertiesLayout.addWidget(self.addPropertyButton, 0)
        
        # Card 3: Card Area for preview
        self.cardArea = CardArea(self.context, self)
        self.cardArea.cardsTitle.setText('现有紫卡')
        self.cardArea.setFilter(None, None, ["riven"])  # Show only Riven cards initially

        self.mainLayout.addWidget(self.basicInfoCard)
        self.mainLayout.addWidget(self.propertiesCard)
        self.mainLayout.addWidget(self.cardArea, 1) # Give it stretch factor

        self._init_slots()
        self._init_weapon_types()
        self._init_riven_ranges()
        self._init_signals()
        self.add_property_editor()
        self.add_property_editor()

    def _init_riven_ranges(self):
        for rr in RivenRange:
            self.riven_range_combo.addItem(RivenRangeToString.get(rr, '未知'), userData=rr)
        self.riven_range_combo.setCurrentText(RivenRangeToString.get(RivenRange.PP))

    def _init_weapon_types(self):
        for wt in WeaponType:
            if wt not in [WeaponType.All]:
                self.weapon_type_combo.addItem(WeaponTypeToString.get(wt, '未知'), userData=wt)
        self.weapon_type_combo.setCurrentText(WeaponTypeToString.get(WeaponType.Rifle))

    def _init_slots(self):
        for slot in Slot:
            self.slot_combo.addItem(SlotToText.get(slot.value, '未知'), userData=slot)

    def _init_signals(self):
        self.addPropertyButton.clicked.connect(self.add_property_editor)
        self.saveButton.clicked.connect(self._save_card)
        self.weapon_type_combo.currentIndexChanged.connect(self.recalculate_property_range)
        self.riven_range_combo.currentIndexChanged.connect(self.recalculate_property_range)

    def _save_card(self):
        card_name = self.name_edit.text()
        if not card_name:
            InfoBar.error('错误', '卡牌名称不能为空!', parent=self.window(), position=InfoBarPosition.TOP, duration=3000)
            return
        
        if get_card_by_name(card_name):
            InfoBar.error('错误', f'卡牌名称 {card_name} 已存在，请使用不同的名称!', parent=self.window(), position=InfoBarPosition.TOP, duration=3000)
            return

        properties = []
        for editor in self.property_editors:
            prop_type = editor.property_type_combo.currentData()
            prop_value_str = editor.property_value_edit.text()
            
            if not prop_value_str:
                InfoBar.error('错误', f'属性 {prop_type.toString()} 的数值不能为空!', parent=self.window(), position=InfoBarPosition.TOP, duration=3000)
                return
            
            try:
                prop_value = float(prop_value_str)
                properties.append(Property.createCardProperty(prop_type, prop_value))
            except ValueError:
                InfoBar.error('错误', f'属性 {prop_type.toString()} 的数值无效!', parent=self.window(), position=InfoBarPosition.TOP, duration=3000)
                return

        if not properties:
            InfoBar.error('错误', '至少需要一个属性!', parent=self.window(), position=InfoBarPosition.TOP, duration=3000)
            return

        slot = self.slot_combo.currentData()
        weapon_type = self.weapon_type_combo.currentData()

        # 创建 CardRiven 对象
        new_riven_card = CardRiven(
            name=card_name,
            properties=properties,
            cost=15,
            slot=slot,
            weaponType=weapon_type
        )

        # 使用 data.cards 中的函数保存
        if save_riven_card(new_riven_card):
            InfoBar.success('成功', f'紫卡 {card_name} 已保存!', parent=self.window(), position=InfoBarPosition.TOP, duration=3000)
            # 触发 cardChanged 信号刷新卡牌区域
            self.context.card_data_changed.emit()
            # 清空输入
            self.name_edit.clear()
            self.slot_combo.setCurrentIndex(0)
            self.weapon_type_combo.setCurrentText(WeaponTypeToString.get(WeaponType.Rifle))
            # 移除所有属性编辑器并添加一个默认的
            for editor in self.property_editors[:]:
                self.remove_property_editor(editor)
            self.add_property_editor()
        else:
            InfoBar.error('保存失败', '保存紫卡时发生未知错误。', parent=self.window(), position=InfoBarPosition.TOP, duration=5000)

    def add_property_editor(self):
        if len(self.property_editors) >= 4:
            return
        
        editor = PropertyEditor(self)
        editor.remove_button.clicked.connect(lambda: self.remove_property_editor(editor))
        editor.property_type_combo.currentIndexChanged.connect(self.recalculate_property_range)
        self.propertiesListLayout.addWidget(editor)
        self.property_editors.append(editor)
        self.update_buttons_state()
        self.recalculate_property_range()

    def remove_property_editor(self, editor):
        if len(self.property_editors) <= 1:
            return

        self.propertiesListLayout.removeWidget(editor)
        editor.deleteLater()
        self.property_editors.remove(editor)
        self.update_buttons_state()

    def update_buttons_state(self):
        self.addPropertyButton.setEnabled(len(self.property_editors) < 4)
        for editor in self.property_editors:
            editor.remove_button.setEnabled(len(self.property_editors) > 2)

    def recalculate_property_range(self):
        weapon_type = self.weapon_type_combo.currentData()
        riven_range = self.riven_range_combo.currentData()
        for editor in self.property_editors:
            prop_type = editor.property_type_combo.currentData()
            if prop_type:
                min_val, max_val = calculate_riven_property_range(prop_type, weapon_type, riven_range)
                editor.property_value_edit.setThreshold((min_val, max_val))
