from PyQt5.QtCore import QObject, pyqtSignal

class AppContext(QObject):
    card_data_changed = pyqtSignal()
    weapon_data_changed = pyqtSignal()

    # 自动化操作所需要触发的信号
    trigger_auto_sprint = pyqtSignal()
    trigger_auto_jump = pyqtSignal()
    trigger_auto_adept_skill = pyqtSignal()
    trigger_auto_finisher_skill = pyqtSignal()

    battleContext = None
    
    def __init__(self):
        super().__init__()
        self.all_cards = []
        self.all_weapons = []

    def load_data(self):
        from data.cards import get_all_cards
        self.all_cards = get_all_cards()
        print(f"成功加载 {len(self.all_cards)} 张卡牌。")

        from data.weapons import get_all_weapons
        self.all_weapons = get_all_weapons()
        print(f"成功加载 {len(self.all_weapons)} 把武器。")

APP_CONTEXT = AppContext()
