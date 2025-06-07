import data.cards as cards
import data.weapons as weapons
from data.env import env, Environment
from core.permutations import getAllPermutations, Pruning, getAllAvailableCards
from core.ivtenum import CardSet
from core.baseclass import EnemyBase, EnemyMaterial, PropertyType, CardRiven, Property, WeaponType
import core.dps as dps
import time

env.reset()
env.SetNum[CardSet.Invasion.value] = 1 # 侵犯光环数量：1
env.SetNum[CardSet.Reverse.value] = 1  # 逆转卡数量：2
env.useNianSkill = True  # 使用年技能
env.nianSkillStrength = 200

enemy = EnemyBase("测试敌人", 120, EnemyMaterial.Mechanical)
enemy.armor = 850
# enemy.setConstantDebuff(PropertyType.Virus, 10) # 挂10层病毒

weapon = weapons.WaterDrop_Prime()
weapon.setCardAtIndex(0, CardRiven("水滴 精密(裂罅)", 
                                   [
                                        Property(PropertyType.CriticalChance, 0, 112),
                                        Property(PropertyType.CriticalDamage, 0, 97),
                                   ], cost=16, weaponType=WeaponType.Rifle))
weapon.updateCurrentProperties()

cards_to_permute, cards_to_combine = getAllAvailableCards(weapon)
all_permutations = getAllPermutations(cards_to_permute, cards_to_combine, 8)
Pruning(all_permutations, env)

max_dps = 0
max_permutation = None
start_time = time.time()
for idx, perm in enumerate(all_permutations):
    # 测试前将敌人身上的debuff清空免得影响DPS计算结果
    enemy.clearDebuff()
    weapon.setCardPermutes(perm)
    weapon.updateCurrentProperties()
    # 计算整个时间内的平均dps
    currentDps = dps.CalculateAverageDPS(weapon, enemy, env)

    if currentDps > max_dps:
        max_dps = currentDps
        max_permutation = perm
        print(f"新的最大DPS: {max_dps:.2f}，卡牌组合: {[card.name for card in perm]}")
end_time = time.time()

print(f"所有 {len(all_permutations)} 个排列已处理完毕。")
print(f'总耗时: {end_time - start_time:.2f}秒')
print("")
env.printEnvironment()
print("=" * 30)
enemy.clearDebuff()
enemy.printEnemyInfo()
print("=" * 30)
print(f"找到的最大DPS: {max_dps:.2f}")
weapon.setCardPermutes(max_permutation)
weapon.updateCurrentProperties()
print("最大DPS对应的武器面板:")
weapon.printAllProperties()
print("=" * 30)
# 计算这个组合下首发伤害
OneHitDamage_Critical = dps.CalculateDamageOnce(weapon, enemy, env, forceCritical=1, forceTrigger=-1)
OneHitDamage_Uncritical = dps.CalculateDamageOnce(weapon, enemy, env, forceCritical=-1, forceTrigger=-1)
print(f"首发伤害（暴击）：{OneHitDamage_Critical:.2f}")
print(f"首发伤害（非暴击）：{OneHitDamage_Uncritical:.2f}")