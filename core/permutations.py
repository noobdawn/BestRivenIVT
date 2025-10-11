# 这个文件负责从武器获取所有可能的卡牌排列
import data.cards as cards
import core.baseclass as baseclass
from data.env import Context
from itertools import combinations, permutations

def isPermutable(card : baseclass.CardBase) -> bool:
    """
    判断卡牌参与排列还是组合
    :param card: 卡牌对象
    :return: 如果卡牌可以进行排列，则返回True，否则返回False
    """
    properties = card.getProperties()
    for prop in properties:
        if prop.propertyType.isElementDamage():
            return True
    return False


def getAllCards(weapon : baseclass.WeaponBase) -> list:
    """
    获取武器上所有可能的卡牌
    :param weapon: 武器对象
    :return: 返回武器上所有可能的卡牌列表
    """
    all_cards = []
    all_cards.extend(cards.CARDS_REPOSITORY[baseclass.WeaponType.All])
    all_cards.extend(cards.CARDS_REPOSITORY[weapon.weaponType])
    return all_cards

def getAllAvailableCards(ctx : Context) -> tuple:
    """
    获取武器上所有可能的卡牌排列
    :param weapon: 武器对象
    :return: 返回用于计算排列和用于计算组合的卡牌元组
    """
    # 获取所有可用的卡牌
    all_cards = getAllCards(ctx.weapon)

    # 带元素伤害类的卡牌是用于计算排列的，其他的计算组合即可
    cards_can_permute = []
    cards_can_combine = []
    cards_must_permute = []
    cards_must_combine = []

    # 先获取武器上已有的卡牌
    for card in ctx.weapon.cards:
        if card is not None:
            if isPermutable(card):
                cards_must_permute.append(card)
            else:
                cards_must_combine.append(card)
                
    for card in all_cards:
        if card in ctx.weapon.cards:
            continue
        if isPermutable(card):
            cards_can_permute.append(card)
        else:
            cards_can_combine.append(card)

    return cards_can_permute, cards_can_combine, cards_must_permute, cards_must_combine

def _getAllPermutations(cards_can_permute : list, cards_can_combine : list, cards_must_permute : list, cards_must_combine : list, max_slots: int) -> list:
    """
    获取所有可能的卡牌排列和组合
    :param cards_can_permute: 可用于排列的卡牌列表
    :param cards_can_combine: 可用于组合的卡牌列表
    :param cards_must_permute: 必须用于排列的卡牌列表
    :param cards_must_combine: 必须用于组合的卡牌列表
    :param max_slots: 最大卡槽数量
    :return: 所有长度为max_slots的卡牌排列
    """
    results = []
    
    must_permute_count = len(cards_must_permute)
    must_combine_count = len(cards_must_combine)
    can_permute_count = len(cards_can_permute)
    can_combine_count = len(cards_can_combine)
    total_must_count = must_permute_count + must_combine_count
    total_can_count = can_permute_count + can_combine_count
    total_count = total_must_count + total_can_count
    if total_count < max_slots:
        max_slots = total_count
    if total_must_count > max_slots:
        raise ValueError("必须使用的卡牌数量超过了最大卡槽数量")
    
    rem_slots = max_slots - total_must_count

    # 迭代所有可能的来自 can_permute 和 can_combine 的卡牌数量组合
    for i in range(rem_slots + 1):
        # i 是从 cards_can_permute 中选择的卡牌数量
        # j 是从 cards_can_combine 中选择的卡牌数量
        j = rem_slots - i

        if i > can_permute_count or j > can_combine_count:
            continue

        # 从 can_permute 中选择 i 张卡牌的所有组合
        for permute_choice in combinations(cards_can_permute, i):
            # 从 can_combine 中选择 j 张卡牌的所有组合
            for combine_choice in combinations(cards_can_combine, j):
                
                # 准备用于排列的卡牌列表
                cards_to_permute = cards_must_permute + list(permute_choice)
                # 准备无需排列的卡牌列表
                cards_to_combine_final = cards_must_combine + list(combine_choice)

                # 生成 cards_to_permute 的所有排列
                for p in permutations(cards_to_permute):
                    results.append(cards_to_combine_final + list(p))

    return results

def getAllPermutations(ctx : Context, max_slots: int) -> list:
    """
    获取所有可能的卡牌排列和组合
    :param ctx: 当前环境上下文
    :param max_slots: 最大卡槽数量
    :return: 所有长度为max_slots的卡牌排列
    """
    weapon = ctx.weapon
    cards_can_permute, cards_can_combine, cards_must_permute, cards_must_combine = getAllAvailableCards(ctx)
    # 在计算排列之前，略微剪枝保证效率
    all_cards = getAllCards(weapon)
    # 如果有魈鬼系列卡牌，则所有组合中都必须包含魈鬼系列卡牌
    # 反之，如果没有魈鬼系列卡牌，则所有组合中都不能包含魈鬼系列卡牌
    ghost_cards = [card for card in all_cards if isinstance(card, baseclass.CardCommon) and card.cardSet == baseclass.CardSet.Ghost]
    if ctx.hasCardSet(baseclass.CardSet.Ghost):
        for ghost_card in ghost_cards:
            if ghost_card not in cards_must_combine:
                cards_must_combine.append(ghost_card)
            if ghost_card in cards_can_combine:
                cards_can_combine.remove(ghost_card)
    else:
        for ghost_card in ghost_cards:
            if ghost_card in cards_can_combine:
                cards_can_combine.remove(ghost_card)
            if ghost_card in cards_must_combine:
                cards_must_combine.remove(ghost_card)        

    return _getAllPermutations(cards_can_permute, cards_can_combine, cards_must_permute, cards_must_combine, max_slots)

# cards_to_permute, cards_to_combine = getAllAvailableCards(weapon)
# all_permutations = getAllPermutations(cards_to_permute, cards_to_combine, 8)
# Pruning(all_permutations, env)

# import copy
# clone_weapon = copy.deepcopy(weapon)

# # 逐个测试各个组合的伤害
# max_dps = 0
# max_permutation = None
# total_permutations = len(all_permutations)
# progress_step = total_permutations // 100 if total_permutations >= 100 else 1
# import time
# start_time = time.time()
# for idx, perm in enumerate(all_permutations):
#     enemy.clearDebuff()
#     weapon.setCardPermutes(perm)
#     weapon.updateCurrentProperties()
#     currentDps = dps.CalculateMagazineDPS(weapon, enemy, env)

#     if currentDps > max_dps:
#         max_dps = currentDps
#         max_permutation = perm
#         print(f"New max DPS: {max_dps:.2f} with cards: {[card.name for card in perm]}")
    
# end_time = time.time()
# print(f'Total time taken: {end_time - start_time:.2f} seconds')
# print(f"Max DPS found: {max_dps:.2f}")
# print(f"All {len(all_permutations)} permutations processed.")

# env.reset()
# env.SetNum[core.CardSet.Ghost.value] = 0  # 魈鬼之眼套装数量
# env.SetNum[core.CardSet.Reverse.value] = 2  # 逆转之心套装数量
# env.SetNum[core.CardSet.Invasion.value] = 1  # 侵犯光环数量
# env.printEnvironment()

# print("")

# enemy = core.EnemyBase("测试敌人", 0, core.EnemyMaterial.Mechanical)
# enemy.armor = 850
# enemy.printEnemyInfo()

# weapon.setCardPermutes(max_permutation)
# weapon.updateCurrentProperties()
# weapon.printAllProperties()
# # # 计算下这个组合下攻击敌人的伤害
# OneHitDamage = dps.CalculateDamageOnce(weapon, enemy, env, forceCritical=True, forceTrigger=-1)
# print(f"One hit damage with max permutation: {OneHitDamage:.2f}")