from qfluentwidgets import (CardWidget, ComboBox, SpinBox, CheckBox, PrimaryPushButton, SubtitleLabel, LineEdit, FluentIcon as FIF)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from core.ivtenum import EnemyMaterial, PropertyType, SkillFlag

class TargetSettingCard(CardWidget):
    """ 靶标设置卡 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('targetSettingCard')

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(20, 10, 20, 10)
        self.vBoxLayout.setSpacing(10)

        self.title = SubtitleLabel('靶标设置')
        self.vBoxLayout.addWidget(self.title)

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
        self.vBoxLayout.addLayout(self.material_layout)

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
        self.vBoxLayout.addLayout(self.armor_layout)

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
        
        self.vBoxLayout.addLayout(self.debuff_layout)

        # 技能易伤
        self.skill_debuff_layout = QVBoxLayout()
        self.skill_debuff_label = SubtitleLabel('技能易伤')
        self.skill_debuff_layout.addWidget(self.skill_debuff_label)

        self.skill_debuff_widgets = {}
        for flag in SkillFlag:
            checkbox = CheckBox(flag.toString())
            self.skill_debuff_layout.addWidget(checkbox)
            self.skill_debuff_widgets[flag] = checkbox

        self.vBoxLayout.addLayout(self.skill_debuff_layout)


class WeaponBuildPage(QFrame):

    def __init__(self, context, parent=None):
        super().__init__(parent=parent)
        self.context = context
        self.setObjectName('weaponBuildPage')

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 20)
        self.vBoxLayout.setSpacing(10)

        self.target_setting_card = TargetSettingCard(self)
        self.vBoxLayout.addWidget(self.target_setting_card)
        self.vBoxLayout.addStretch(1)

        # Connect signals
        self.target_setting_card.material_combo.currentIndexChanged.connect(self.on_target_changed)
        self.target_setting_card.armor_spinbox.valueChanged.connect(self.on_target_changed)
        for prop, (checkbox, spinbox) in self.target_setting_card.debuff_widgets.items():
            checkbox.stateChanged.connect(self.on_target_changed)
            spinbox.valueChanged.connect(self.on_target_changed)
        for flag, checkbox in self.target_setting_card.skill_debuff_widgets.items():
            checkbox.stateChanged.connect(self.on_target_changed)
        
        self.on_target_changed()

    def on_target_changed(self):
        if self.context.battleContext is None:
            return

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
        
        # self.context.battleContext.printEnvironment() # for debugging
