from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import SubtitleLabel, CheckBox
from .component.foldable_card_widget import FoldableCardWidget
from .component.value_edit import ValueEdit
from core.context import APP_CONTEXT, AppContext

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

        self.auto_sprint_checkbox = CheckBox('开启自动冲刺（热键：END）', self)
        self.auto_sprint_in_game_checkbox = CheckBox('仅在《驱入虚空》窗口激活时', self)
        self.auto_sprint_in_game_checkbox.setChecked(True)
        sprint_layout.addWidget(self.auto_sprint_checkbox)
        sprint_layout.addWidget(self.auto_sprint_in_game_checkbox)

        sprint_control_layout = QHBoxLayout()
        sprint_control_layout.addWidget(QLabel('冲刺间隔(秒):', self))
        self.sprint_interval_edit = ValueEdit('float', threshold=(0.1, 10.0))
        self.sprint_interval_edit.setText('0.1')
        sprint_control_layout.addWidget(self.sprint_interval_edit)
        sprint_control_layout.addStretch(1)
        sprint_layout.addLayout(sprint_control_layout)

        self.autoSprintCard.contentLayout().addWidget(sprint_content_widget)
        self.vBoxLayout.addWidget(self.autoSprintCard)

        # Auto Jump Card
        self.autoJumpCard = FoldableCardWidget('自动跳跃', self)
        jump_content_widget = QWidget()
        jump_layout = QVBoxLayout(jump_content_widget)
        jump_layout.setContentsMargins(0, 0, 0, 0)

        self.auto_jump_checkbox = CheckBox('开启自动跳跃（热键：HOME）', self)
        self.auto_jump_in_game_checkbox = CheckBox('仅在《驱入虚空》窗口激活时', self)
        self.auto_jump_in_game_checkbox.setChecked(True)
        jump_layout.addWidget(self.auto_jump_checkbox)
        jump_layout.addWidget(self.auto_jump_in_game_checkbox)

        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel('跳跃间隔(秒):', self))
        self.jump_interval_edit = ValueEdit('float', threshold=(0.1, 10.0))
        self.jump_interval_edit.setText('1.0')
        control_layout.addWidget(self.jump_interval_edit)
        control_layout.addStretch(1)
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

        self.init_automation()

    def init_automation(self):        
        # Automation
        self.auto_jump_checkbox.stateChanged.connect(self.toggle_auto_jump)
        self.jump_interval_edit.textChanged.connect(self.update_jump_interval)

        # Pass the state of "Only activate in game window" checkboxes to workers
        self.auto_jump_in_game_checkbox.stateChanged.connect(
            lambda state: setattr(self.auto_jump_worker, 'check_only_in_game', state))

        self.auto_sprint_checkbox.stateChanged.connect(self.toggle_auto_sprint)
        self.sprint_interval_edit.textChanged.connect(self.update_sprint_interval)
        
        self.auto_sprint_in_game_checkbox.stateChanged.connect(
            lambda state: setattr(self.auto_sprint_worker, 'check_only_in_game', state)
        )

        self.auto_jump_worker = APP_CONTEXT.auto_jump_worker
        self.auto_sprint_worker = APP_CONTEXT.auto_sprint_worker
        APP_CONTEXT.hotkeyListener.home_pressed.connect(self.toggle_auto_jump_hotkey)
        APP_CONTEXT.hotkeyListener.end_pressed.connect(self.toggle_auto_sprint_hotkey)

    def toggle_auto_jump(self, state):
        if state:
            interval_text = self.jump_interval_edit.text()
            self.auto_jump_worker.set_interval(interval_text)
            self.auto_jump_worker.start()
        else:
            self.auto_jump_worker.stop()

    def toggle_auto_sprint(self, state):
        if state:
            self.auto_sprint_worker.start()
        else:
            self.auto_sprint_worker.stop()

    def update_jump_interval(self, text):
        self.auto_jump_worker.set_interval(text)

    def update_sprint_interval(self, text):
        self.auto_sprint_worker.set_interval(text)

    def toggle_auto_jump_hotkey(self):
        is_checked = self.auto_jump_checkbox.isChecked()
        self.auto_jump_checkbox.setChecked(not is_checked)

    def toggle_auto_sprint_hotkey(self):
        is_checked = self.auto_sprint_checkbox.isChecked()
        self.auto_sprint_checkbox.setChecked(not is_checked)

    def closeEvent(self, event):
        APP_CONTEXT.hotkeyListener.stop()
        super().closeEvent(event)