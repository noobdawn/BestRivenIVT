from qfluentwidgets import (ComboBox, SpinBox, CheckBox, PrimaryPushButton, SubtitleLabel, LineEdit, FluentIcon as FIF, DoubleSpinBox, PushButton, TransparentToolButton, CardWidget)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtGui import QFont
from core.ivtenum import EnemyMaterial, PropertyType, SkillFlag, CardSet, AvailableCardSets
from .component.foldable_card_widget import FoldableCardWidget
from core.baseclass import WeaponBase
from data.env import Context
import data.armors as armors
from core.dps import CalculateAverageDPS, CalculateMagazineDamage, CalculateMagazineDPS, CalculateDamageOnce

class WeaponPropertyCard(CardWidget):
    """ 武器属性展示卡 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('weaponPropertyCard')

        self.content_layout = QVBoxLayout(self)
        self.content_layout.setSpacing(4)
        
        self.title = SubtitleLabel('武器属性', self)
        self.content_layout.addWidget(self.title)

        self.property_layout = QVBoxLayout()
        self.content_layout.addLayout(self.property_layout)
        self.content_layout.addStretch(1)

        self.property_labels = {}

        self.setFixedWidth(400)

    def update_properties(self, weapon: WeaponBase, single_burst_damage, single_burst_dps, average_dps, one_hit_critical_damage, one_hit_non_critical_damage):

        # Clear old labels
        for label in self.property_labels.values():
            self.property_layout.removeWidget(label)
            label.deleteLater()
        self.property_labels.clear()

        # Add new properties
        self._add_property_label('首发暴击伤害', str(one_hit_critical_damage), tooltip='若暴击率超过100%则为下一等级暴击伤害')
        self._add_property_label('首发非暴击伤害', str(one_hit_non_critical_damage), tooltip='若暴击率超过100%则为原等级暴击伤害')
        self._add_property_label('单次爆发伤害量', str(single_burst_damage), tooltip='单个弹匣造成的总伤害')
        self._add_property_label('单次爆发DPS', str(single_burst_dps), tooltip='单个弹匣造成的每秒伤害')
        self._add_property_label('平均DPS', str(average_dps), tooltip='计入换弹时间后的每秒伤害')

        # Update total damage
        total_damage = weapon.currentProperties.getTotalDamage()
        self._add_property_label('总伤害', f'{total_damage:.2f}')


        # Update other properties
        for prop_type, prop_obj in weapon.currentProperties.datas.items():
            value = prop_obj.get()
            if value != 0:
                # Format based on property type
                if prop_type in [PropertyType.CriticalChance, PropertyType.TriggerChance, PropertyType.CriticalDamage, PropertyType.DebuffDuration]:
                    display_value = f'{(value / 100):.2%}'
                elif prop_type in [PropertyType.MultiStrike]:
                     display_value = f'{value:.2f}x'
                elif prop_type in [PropertyType.MagazineSize]:
                    display_value = f'{int(round(value))}'
                elif prop_type in [PropertyType.ReloadTime]:
                    display_value = f'{value:.2f}s'
                elif prop_type.isDamage():
                    display_value = f'{value:.2f}'
                else:
                    display_value = f'{value:.2f}'
                
                self._add_property_label(prop_type.toString(), display_value)

    def _add_property_label(self, name, value, tooltip=None):
        h_layout = QHBoxLayout()
        name_label = QLabel(name, self)
        font = QFont()
        font.setPointSize(9)
        name_label.setFont(font)
        h_layout.addWidget(name_label)

        if tooltip:
            info_label = QLabel(self)
            info_label.setPixmap(FIF.INFO.icon().pixmap(16, 16))
            info_label.setToolTip(tooltip)
            h_layout.addWidget(info_label)

        h_layout.addStretch(1)
        
        value_label = QLabel(str(value), self)
        value_label.setFont(font)
        h_layout.addWidget(value_label)
        
        # Use a QWidget as a container for the layout
        container_widget = QWidget()
        container_widget.setLayout(h_layout)
        
        self.property_layout.addWidget(container_widget)
        self.property_labels[name] = container_widget # Store the container to remove later

class WeaponSelectionCard(CardWidget):
    """ 武器选择卡 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('weaponSelectionCard')

        self.content_layout = QVBoxLayout(self)
        self.content_layout.setSpacing(10)

        self.weapon_layout = QHBoxLayout()
        self.weapon_label = SubtitleLabel('选择武器', self)
        self.weapon_combo = ComboBox(self)
        
        self.weapon_layout.addWidget(self.weapon_label)
        self.weapon_layout.addStretch(1)
        self.weapon_layout.addWidget(self.weapon_combo)
        
        self.content_layout.addLayout(self.weapon_layout)

class RoleSettingCard(FoldableCardWidget):
    """ 角色设置卡 """

    def __init__(self, parent=None):
        super().__init__('角色设置', parent)
        self.setObjectName('roleSettingCard')

        content_layout = self.contentLayout()
        content_layout.setSpacing(10)

        # 角色状态
        self.state_layout = QHBoxLayout()
        self.is_moving_checkbox = CheckBox('移动中', self)
        self.is_in_air_checkbox = CheckBox('空中', self)
        self.sniper_combo_label = SubtitleLabel('狙击倍率', self)
        self.sniper_combo_spinbox = DoubleSpinBox(self)
        self.sniper_combo_spinbox.setRange(1.0, 10.0)
        self.sniper_combo_spinbox.setSingleStep(0.1)
        self.sniper_combo_spinbox.setValue(1.0)

        self.state_layout.addWidget(self.is_moving_checkbox)
        self.state_layout.addWidget(self.is_in_air_checkbox)
        self.state_layout.addStretch(1)
        self.state_layout.addWidget(self.sniper_combo_label)
        self.state_layout.addWidget(self.sniper_combo_spinbox)
        content_layout.addLayout(self.state_layout)

        # 技能强度
        self.skill_strength_layout = QHBoxLayout()
        self.skill_strength_label = SubtitleLabel('技能强度', self)
        self.skill_strength_spinbox = SpinBox(self)
        self.skill_strength_spinbox.setRange(0, 9999)
        self.skill_strength_spinbox.setValue(100)
        self.skill_strength_layout.addWidget(self.skill_strength_label)
        self.skill_strength_layout.addStretch(1)
        self.skill_strength_layout.addWidget(self.skill_strength_spinbox)
        content_layout.addLayout(self.skill_strength_layout)

        # 套卡设置
        self.card_set_layout = QVBoxLayout()
        self.card_set_label = SubtitleLabel('套卡设置', self)
        self.card_set_layout.addWidget(self.card_set_label)
        
        self.card_set_widgets = []
        self.card_set_list_layout = QVBoxLayout()
        self.add_card_set_button = PushButton(FIF.ADD, '添加套卡', self)
        self.add_card_set_button.clicked.connect(self.add_card_set_row)

        self.card_set_layout.addLayout(self.card_set_list_layout)
        self.card_set_layout.addWidget(self.add_card_set_button)
        content_layout.addLayout(self.card_set_layout)

    def add_card_set_row(self, card_set_data=None, count=0):
        row_layout = QHBoxLayout()
        combo = ComboBox(self)
        for cs in AvailableCardSets:
            combo.addItem(cs.toString(), userData=cs)
        
        spinbox = SpinBox(self)
        spinbox.setRange(1, 10)
        
        remove_button = TransparentToolButton(FIF.REMOVE, self)

        row_layout.addWidget(combo)
        row_layout.addWidget(spinbox)
        row_layout.addStretch(1)
        row_layout.addWidget(remove_button)

        self.card_set_list_layout.addLayout(row_layout)
        widget_tuple = (combo, spinbox, remove_button, row_layout)
        self.card_set_widgets.append(widget_tuple)

        remove_button.clicked.connect(lambda: self.remove_card_set_row(widget_tuple))
        
        combo.currentIndexChanged.connect(self.parent().parent().on_weapon_changed)
        spinbox.valueChanged.connect(self.parent().parent().on_weapon_changed)

        if card_set_data:
            combo.setCurrentIndex(combo.findData(card_set_data))
            spinbox.setValue(count)

        self.parent().parent().on_weapon_changed()

    def remove_card_set_row(self, widget_tuple):
        combo, spinbox, remove_button, row_layout = widget_tuple
        
        combo.currentIndexChanged.connect(self.parent().parent().on_weapon_changed)
        spinbox.valueChanged.connect(self.parent().parent().on_weapon_changed)        

        # Remove widgets from layout
        while row_layout.count():
            child = row_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.card_set_list_layout.removeItem(row_layout)
        row_layout.deleteLater()
        self.card_set_widgets.remove(widget_tuple)
        
        self.parent().parent().on_weapon_changed()

class TargetSettingCard(FoldableCardWidget):
    """ 靶标设置卡 """

    def __init__(self, parent=None):
        super().__init__('靶标设置', parent)
        self.setObjectName('targetSettingCard')

        content_layout = self.contentLayout()
        content_layout.setSpacing(10)

        # 靶标材质
        self.material_layout = QHBoxLayout()
        self.material_label = SubtitleLabel('靶标材质')
        self.material_combo = ComboBox()
        for material in EnemyMaterial:
            self.material_combo.addItem(material.toString(), userData=material)
        self.material_combo.setCurrentIndex(EnemyMaterial.Void.value)
        self.material_layout.addWidget(self.material_label)
        self.material_layout.addStretch(1)
        self.material_layout.addWidget(self.material_combo)
        content_layout.addLayout(self.material_layout)

        # 护甲
        self.armor_layout = QHBoxLayout()
        self.armor_label = SubtitleLabel('护甲')
        self.armor_spinbox = SpinBox()
        self.armor_spinbox.setRange(0, 99999)
        self.armor_spinbox.setValue(850)
        self.armor_info_label = QLabel()
        self.armor_info_label.setPixmap(FIF.INFO.icon().pixmap(16, 16))
        self.armor_info_label.setToolTip("参考：120级阿尔法")
        self.armor_layout.addWidget(self.armor_label)
        self.armor_layout.addStretch(1)
        self.armor_layout.addWidget(self.armor_spinbox)
        self.armor_layout.addWidget(self.armor_info_label)
        content_layout.addLayout(self.armor_layout)

        # 元素异常
        self.debuff_layout = QVBoxLayout()
        self.debuff_label = SubtitleLabel('元素异常')
        self.debuff_layout.addWidget(self.debuff_label)

        self.debuffs = {
            PropertyType.Cold: {"name": "冰冻", "max": 9},
            PropertyType.Radiation: {"name": "辐射", "max": 10},
            PropertyType.Virus: {"name": "病毒", "max": 10},
            PropertyType.Fire: {"name": "热波", "max": 1}
        }

        self.debuff_widgets = {}
        for prop, info in self.debuffs.items():
            layout = QHBoxLayout()
            checkbox = CheckBox(info["name"])
            spinbox = SpinBox()
            spinbox.setRange(0, info["max"])
            spinbox.setEnabled(False)
            checkbox.stateChanged.connect(lambda state, s=spinbox: s.setEnabled(state))
            
            layout.addWidget(checkbox)
            layout.addStretch(1)
            layout.addWidget(spinbox)
            self.debuff_layout.addLayout(layout)
            self.debuff_widgets[prop] = (checkbox, spinbox)
        
        content_layout.addLayout(self.debuff_layout)

        # 技能易伤
        self.skill_debuff_layout = QVBoxLayout()
        self.skill_debuff_label = SubtitleLabel('技能易伤')
        self.skill_debuff_layout.addWidget(self.skill_debuff_label)

        self.skill_debuff_widgets = {}
        for flag in SkillFlag:
            checkbox = CheckBox(flag.toString())
            self.skill_debuff_layout.addWidget(checkbox)
            self.skill_debuff_widgets[flag] = checkbox

        content_layout.addLayout(self.skill_debuff_layout)


class WeaponBuildPage(QFrame):

    def __init__(self, context, parent=None):
        super().__init__(parent=parent)
        self.context = context
        self.setObjectName('weaponBuildPage')

        # Main layout
        self.main_h_layout = QHBoxLayout(self)
        self.main_h_layout.setContentsMargins(10, 10, 10, 10)
        self.main_h_layout.setSpacing(10)

        # Left layout for settings cards
        self.left_widget = QWidget(self)
        self.left_v_layout = QVBoxLayout(self.left_widget)
        self.left_v_layout.setContentsMargins(0, 0, 0, 0)
        self.left_v_layout.setSpacing(10)

        self.weapon_selection_card = WeaponSelectionCard(self)
        self.target_setting_card = TargetSettingCard(self)
        self.role_setting_card = RoleSettingCard(self)
        
        self.left_v_layout.addWidget(self.weapon_selection_card)
        self.left_v_layout.addWidget(self.target_setting_card)
        self.left_v_layout.addWidget(self.role_setting_card)
        self.left_v_layout.addStretch(1)

        # Right layout for property display
        self.weapon_property_card = WeaponPropertyCard(self)

        self.main_h_layout.addWidget(self.left_widget, 1)
        self.main_h_layout.addWidget(self.weapon_property_card, 2)

        self.load_weapons_to_combo()
        self.context.weapon_data_changed.connect(self.load_weapons_to_combo)

        # Connect signals
        self.weapon_selection_card.weapon_combo.currentIndexChanged.connect(self.on_weapon_changed)
        self.target_setting_card.material_combo.currentIndexChanged.connect(self.on_target_changed)
        self.target_setting_card.armor_spinbox.valueChanged.connect(self.on_target_changed)
        for prop, (checkbox, spinbox) in self.target_setting_card.debuff_widgets.items():
            checkbox.stateChanged.connect(self.on_target_changed)
            spinbox.valueChanged.connect(self.on_target_changed)
        for flag, checkbox in self.target_setting_card.skill_debuff_widgets.items():
            checkbox.stateChanged.connect(self.on_target_changed)
        
        self.role_setting_card.is_moving_checkbox.stateChanged.connect(self.on_role_changed)
        self.role_setting_card.is_in_air_checkbox.stateChanged.connect(self.on_role_changed)
        self.role_setting_card.sniper_combo_spinbox.valueChanged.connect(self.on_role_changed)
        self.role_setting_card.skill_strength_spinbox.valueChanged.connect(self.on_role_changed)
        # Card set signals are connected in add_card_set_row

        self.on_weapon_changed()
        self.on_target_changed()
        self.on_role_changed()

    def update_weapon_properties_display(self):
        weapon = self.context.battleContext.weapon
        weapon.updateCurrentProperties()

        ctx = self.context.battleContext

        single_burst_damage = CalculateMagazineDamage(ctx)
        single_burst_dps = CalculateMagazineDPS(ctx)
        average_dps = CalculateAverageDPS(ctx)
        one_hit_critical_damage = CalculateDamageOnce(ctx, forceCritical=1, forceTrigger=-1)
        one_hit_non_critical_damage = CalculateDamageOnce(ctx, forceCritical=-1, forceTrigger=-1)

        self.weapon_property_card.update_properties(weapon, single_burst_damage, single_burst_dps, average_dps, one_hit_critical_damage, one_hit_non_critical_damage)

    def load_weapons_to_combo(self):
        self.weapon_selection_card.weapon_combo.clear()
        for weapon in self.context.all_weapons:
            self.weapon_selection_card.weapon_combo.addItem(weapon.name, userData=weapon)

    def on_weapon_changed(self):
        selected_weapon = self.weapon_selection_card.weapon_combo.currentData()
        self.context.battleContext = Context(armors.Shouzhanqibing(), selected_weapon)

        if selected_weapon:
            # self.context.battleContext.SetWeapon(selected_weapon)
            self.update_weapon_properties_display()


    def on_role_changed(self):

        # Update move state
        self.context.battleContext.character.moveState.isMoving = self.role_setting_card.is_moving_checkbox.isChecked()
        self.context.battleContext.character.moveState.isInAir = self.role_setting_card.is_in_air_checkbox.isChecked()
        self.context.battleContext.character.moveState.sniperComboMulti = self.role_setting_card.sniper_combo_spinbox.value()
        self.context.battleContext.SetCharacterSkillStrength(self.role_setting_card.skill_strength_spinbox.value())
        # Update card sets
        # First, reset all card sets to 0
        for cs in CardSet:
            if cs != CardSet.Unset:
                self.context.battleContext.SetCardSetNum(cs, 0)
        
        # Then, set the numbers from the UI
        for combo, spinbox, _, _ in self.role_setting_card.card_set_widgets:
            card_set = combo.currentData()
            count = spinbox.value()
            self.context.battleContext.SetCardSetNum(card_set, count)

        self.update_weapon_properties_display()

    def on_target_changed(self):
        # Update target material
        material = self.target_setting_card.material_combo.currentData()
        self.context.battleContext.target.material = material

        # Update armor
        armor = self.target_setting_card.armor_spinbox.value()
        self.context.battleContext.target.armor = armor

        # Update elemental debuffs
        for prop, (checkbox, spinbox) in self.target_setting_card.debuff_widgets.items():
            count = spinbox.value() if checkbox.isChecked() else 0
            self.context.battleContext.SetTargetElementDebuff(prop, count)

        # Update skill debuffs
        for flag, checkbox in self.target_setting_card.skill_debuff_widgets.items():
            is_active = checkbox.isChecked()
            self.context.battleContext.SetTargetSkillDebuff(flag, is_active)
        
        self.update_weapon_properties_display()
