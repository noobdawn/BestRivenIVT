import json
from core.baseclass import CardCommon, Property
from core.ivtenum import PropertyType, WeaponType, SubWeaponType, CardSet

def _load_cards_from_json(file_path='data/card.json'):
    """
    (内部函数) 从JSON文件中加载卡牌数据并创建CardCommon对象列表。
    """
    all_cards = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"错误: 无法加载或解析卡牌数据文件 '{file_path}': {e}")
        return []

    for card_data in data:
        # 解析属性
        properties = []
        for prop_data in card_data.get('properties', []):
            try:
                prop_type = PropertyType[prop_data['type']]
                prop_value = prop_data['value']
                properties.append(Property.createCardProperty(prop_type, prop_value))
            except KeyError:
                print(f"警告: 在卡牌 '{card_data['name']}' 中遇到未知的属性类型 '{prop_data.get('type')}'。已跳过。")
                continue

        # 解析武器类型
        try:
            weapon_type = WeaponType.fromString(card_data.get('mainWeapon', 'All'))
        except KeyError:
            weapon_type = WeaponType.All
        
        try:
            sub_weapon_type = SubWeaponType.fromString(card_data.get('subWeapon', 'All'))
        except KeyError:
            sub_weapon_type = SubWeaponType.Null

        # 解析卡牌套装
        card_set_str = card_data.get('cardSet')
        card_set = CardSet[card_set_str] if card_set_str and card_set_str in CardSet.__members__ else CardSet.Unset

        # 创建卡牌对象
        card = CardCommon(
            name=card_data['name'],
            properties=properties,
            cost=card_data.get('cost', 0),
            weaponType=weapon_type,
            weaponSubType=sub_weapon_type,
            cardSet=card_set
        )
        all_cards.append(card)

    return all_cards

# 在模块加载时就准备好所有卡牌数据
ALL_CARDS = _load_cards_from_json()

def get_all_cards():
    """
    返回所有已加载的卡牌列表。
    """
    return ALL_CARDS

def get_cards_by_weapon_type(weapon_type: WeaponType, sub_weapon_type: SubWeaponType = SubWeaponType.Null):
    """
    根据武器类型和子类型筛选卡牌。
    """
    return [
        card for card in ALL_CARDS
        if (card.weaponType == WeaponType.All or card.weaponType == weapon_type) and \
           (card.subWeaponType == SubWeaponType.Null or card.subWeaponType == sub_weapon_type)
    ]

def get_card_by_name(name: str) -> CardCommon | None:
    """
    根据卡牌名称获取对应的卡牌对象。
    """
    for card in ALL_CARDS:
        if card.name == name:
            return card
    return None
