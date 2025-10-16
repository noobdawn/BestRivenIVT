import json
import os
from core.baseclass import CardBase, CardCommon, CardRiven, Property
from core.ivtenum import PropertyType, WeaponType, SubWeaponType, CardSet, Slot

def _load_cards_from_json(file_paths=['data/card.json', 'data/riven.json']):
    """
    (内部函数) 从多个JSON文件中加载卡牌数据并创建Card对象列表。
    """
    all_cards = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # riven.json可能不存在，所以只打印警告而不是错误
            if 'riven.json' in file_path and isinstance(e, FileNotFoundError):
                print(f"信息: 未找到紫卡数据文件 '{file_path}'，将跳过。")
            else:
                print(f"错误: 无法加载或解析卡牌数据文件 '{file_path}': {e}")
            continue # 继续处理下一个文件

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
            
            # 解析极性
            slot_val = card_data.get('slot')
            slot = Slot(slot_val) if slot_val is not None else None

            # 根据 isRiven 字段创建不同类型的卡牌对象
            is_riven = card_data.get('isRiven', False)
            
            if is_riven:
                card = CardRiven(
                    name=card_data['name'],
                    properties=properties,
                    weaponType=weapon_type,
                    cost=card_data.get('cost', 0),
                    slot=slot
                )
            else:
                card = CardCommon(
                    name=card_data['name'],
                    properties=properties,
                    cost=card_data.get('cost', 0),
                    weaponType=weapon_type,
                    weaponSubType=sub_weapon_type,
                    cardSet=card_set,
                    slot=slot
                )
                card.isPrime = card_data.get('isPrime', False)
            
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
        if isinstance(card, CardBase) and \
           (card.weaponType == WeaponType.All or card.weaponType == weapon_type) and \
           (card.subWeaponType == SubWeaponType.Null or card.subWeaponType == sub_weapon_type)
    ]

def get_card_by_name(name: str) -> CardBase | None:
    """
    根据卡牌名称获取对应的卡牌对象。
    """
    for card in ALL_CARDS:
        if card.name == name:
            return card
    return None

def save_riven_card(card: CardRiven) -> bool:
    """
    将一张新的紫卡数据保存到 data/riven.json 文件中。
    如果文件不存在，则会创建它。
    返回一个布尔值表示操作是否成功。
    """
    card_data = {
        'name': card.name,
        'properties': [{'type': p.propertyType.name, 'value': p.addon} for p in card.properties],
        'cost': card.cost,
        'slot': card.slot.value if card.slot else None,
        'isRiven': True,
        "mainWeapon": "All",
        "subWeapon": "All",
    }

    riven_file_path = 'data/riven.json'
    all_rivens = []
    
    # 1. 读取已有的紫卡
    if os.path.exists(riven_file_path):
        try:
            with open(riven_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    all_rivens = json.loads(content)
                # 确保数据是列表格式
                if not isinstance(all_rivens, list):
                    all_rivens = []
        except json.JSONDecodeError:
            # 文件损坏或为空
            all_rivens = []
    
    # 2. 添加新的紫卡
    all_rivens.append(card_data)

    # 3. 写回文件
    try:
        with open(riven_file_path, 'w', encoding='utf-8') as f:
            json.dump(all_rivens, f, ensure_ascii=False, indent=4)
        
        # 更新全局卡牌列表
        global ALL_CARDS
        ALL_CARDS.append(card)
        
        return True
    except Exception as e:
        print(f"错误: 保存紫卡失败: {e}")
        return False

def delete_riven_card(name: str) -> bool:
    """
    根据名称删除 data/riven.json 文件中的一张紫卡。
    返回一个布尔值表示操作是否成功。
    """
    riven_file_path = 'data/riven.json'
    
    if not os.path.exists(riven_file_path):
        print(f"警告: 紫卡文件 '{riven_file_path}' 不存在，无法删除。")
        return False

    all_rivens = []
    # 1. 读取已有的紫卡
    try:
        with open(riven_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if content:
                all_rivens = json.loads(content)
            if not isinstance(all_rivens, list):
                print(f"警告: 紫卡文件 '{riven_file_path}' 格式不正确，应为列表。")
                return False
    except json.JSONDecodeError:
        print(f"警告: 紫卡文件 '{riven_file_path}' 解析失败。")
        return False

    # 2. 查找并准备删除
    card_to_remove_json = None
    for card_json in all_rivens:
        if card_json.get('name') == name:
            card_to_remove_json = card_json
            break
    
    if not card_to_remove_json:
        print(f"信息: 未在 {riven_file_path} 中找到名为 '{name}' 的紫卡。")
        return False

    all_rivens.remove(card_to_remove_json)

    # 3. 写回文件
    try:
        with open(riven_file_path, 'w', encoding='utf-8') as f:
            json.dump(all_rivens, f, ensure_ascii=False, indent=4)
        
        # 4. 从全局卡牌列表中移除
        global ALL_CARDS
        card_to_remove_global = None
        for card in ALL_CARDS:
            if card.name == name and isinstance(card, CardRiven):
                card_to_remove_global = card
                break
        
        if card_to_remove_global:
            ALL_CARDS.remove(card_to_remove_global)
            
        return True
    except Exception as e:
        print(f"错误: 删除并保存紫卡失败: {e}")
        return False

