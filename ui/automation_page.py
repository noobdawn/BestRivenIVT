from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import SubtitleLabel, CheckBox
from .component.foldable_card_widget import FoldableCardWidget
from .component.value_edit import ValueEdit

class AutomationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('automationPage')

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(SubtitleLabel('自动化'))

        # Auto Sprint Card
        self.autoSprintCard = FoldableCardWidget('自动冲刺', self)
        sprint_content_widget = QWidget()
        sprint_layout = QVBoxLayout(sprint_content_widget)
        sprint_layout.setContentsMargins(0, 0, 0, 0)
        self.auto_sprint_checkbox = CheckBox('开启自动冲刺', self)
        sprint_layout.addWidget(self.auto_sprint_checkbox)
        self.autoSprintCard.contentLayout().addWidget(sprint_content_widget)
        self.vBoxLayout.addWidget(self.autoSprintCard)

        # Auto Jump Card
        self.autoJumpCard = FoldableCardWidget('自动跳跃', self)
        jump_content_widget = QWidget()
        jump_layout = QVBoxLayout(jump_content_widget)
        jump_layout.setContentsMargins(0, 0, 0, 0)

        self.auto_jump_checkbox = CheckBox('开启自动跳跃', self)
        
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel('跳跃间隔(秒):', self))
        self.jump_interval_edit = ValueEdit('float', threshold=(0.1, 10.0))
        self.jump_interval_edit.setText('1.0')
        control_layout.addWidget(self.jump_interval_edit)
        control_layout.addStretch(1)

        jump_layout.addWidget(self.auto_jump_checkbox)
        jump_layout.addLayout(control_layout)
        
        self.autoJumpCard.contentLayout().addWidget(jump_content_widget)
        self.vBoxLayout.addWidget(self.autoJumpCard)

        # Auto Adept Skill Card
        self.autoAdeptSkillCard = FoldableCardWidget('自动释放信手技', self)
        self.autoAdeptSkillCard.contentLayout().addWidget(
            QLabel('这里是关于自动释放信手技功能的设置说明。')
        )
        self.vBoxLayout.addWidget(self.autoAdeptSkillCard)

        # Auto Finisher Skill Card
        self.autoFinisherSkillCard = FoldableCardWidget('自动释放破阵技', self)
        self.autoFinisherSkillCard.contentLayout().addWidget(
            QLabel('这里是关于自动释放破阵技功能的设置说明。')
        )
        self.vBoxLayout.addWidget(self.autoFinisherSkillCard)

        self.vBoxLayout.addStretch(1)
