class AppContext:
    def __init__(self):
        self.all_cards = []

    def load_data(self):
        from data.cards import get_all_cards
        self.all_cards = get_all_cards()
        print(f"成功加载 {len(self.all_cards)} 张卡牌。")

APP_CONTEXT = AppContext()
