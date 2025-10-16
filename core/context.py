from PyQt5.QtCore import QObject, pyqtSignal

class AppContext(QObject):
    card_data_changed = pyqtSignal()
    battleContext = None
    
    def __init__(self):
        super().__init__()
        self.all_cards = []

    def load_data(self):
        from data.cards import get_all_cards
        self.all_cards = get_all_cards()
        print(f"成功加载 {len(self.all_cards)} 张卡牌。")

APP_CONTEXT = AppContext()
