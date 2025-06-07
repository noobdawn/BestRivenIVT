# 这个文件负责从武器获取所有可能的卡牌排列
import data.cards as cards
import core.baseclass as baseclass
import core.dps
from data.env import env, Environment
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

def getAllAvailableCards(weapon : baseclass.WeaponBase) -> tuple:
    """
    获取武器上所有可能的卡牌排列
    :param weapon: 武器对象
    :return: 返回用于计算排列和用于计算组合的卡牌元组
    """
    # 获取所有可用的卡牌
    all_cards = []
    all_cards.extend(cards.CARDS_REPOSITORY[baseclass.WeaponType.All])
    all_cards.extend(cards.CARDS_REPOSITORY[weapon.weaponType])

    # 带元素伤害类的卡牌是用于计算排列的，其他的计算组合即可
    cards_to_permute = []
    cards_to_combine = []
    for card in all_cards:
        if isPermutable(card):
            cards_to_permute.append(card)
        else:
            cards_to_combine.append(card)

    # 先获取武器上已有的卡牌
    cards_in_weapon = []
    for card in weapon.cards:
        if card is not None:
            if card in cards_to_permute:
                cards_to_permute.remove(card)
            elif card in cards_to_combine:
                cards_to_combine.remove(card)
            else:
                if isinstance(card, cards.CardRiven):
                    if isPermutable(card):
                        cards_to_permute.append(card)
                    else:
                        cards_to_combine.append(card)

    return cards_to_permute, cards_to_combine


# 剪枝
def Pruning(permutations : list, env : Environment) -> None:
    """
    对卡牌排列进行剪枝
    :param permutations: 卡牌排列列表
    """
    # 如果环境中携带了魈鬼系列卡牌，则所有排列中都必须包含魈鬼之眼
    if env.SetNum[baseclass.CardSet.Ghost.value] > 0:
        for i in range(len(permutations) - 1, -1, -1):
            if not any(isinstance(card, baseclass.CardCommon) and card.cardSet == baseclass.CardSet.Ghost for card in permutations[i]):
                del permutations[i]
    else:
        # 如果没有魈鬼之眼，则所有排列中都不能包含魈鬼之眼
        for i in range(len(permutations) - 1, -1, -1):
            if any(isinstance(card, baseclass.CardCommon) and card.cardSet == baseclass.CardSet.Ghost for card in permutations[i]):
                del permutations[i]

def getAllPermutations(cards_to_permute : list, cards_to_combine : list, max_slots: int) -> list:
    """
    获取所有可能的卡牌排列和组合
    :param cards_to_permute: 可进行排列的卡牌列表
    :param cards_to_combine: 可进行组合的卡牌列表
    :param max_slots: 最大卡槽数量
    :return: 所有长度为max_slots的卡牌排列
    """
    results = []

    for permute_len in range(0, max_slots + 1):
        if permute_len > len(cards_to_permute):
            break
        combine_len = max_slots - permute_len
        if combine_len > len(cards_to_combine):
            continue
        for permute in permutations(cards_to_permute, permute_len):
            for combine in combinations(cards_to_combine, combine_len):
                result = list(permute) + list(combine)
                results.append(result)

    return results

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