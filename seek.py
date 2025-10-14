from data.env import *
import data.cards as cards
import data.weapons as weapons
import data.armors as armors
from core.permutations import getAllPermutations
import core.dps as dps

weapon = weapons.IceFall_Prime()
armor = armors.Yinniaoguilin()
ctx = Context(armor, weapon)
ctx.SetCardSetNum(CardSet.Invasion, 2)
ctx.SetCharacterSkillStrength(200)
ctx.SetTargetSkillDebuff(SkillFlag.Qianyinfeidan, True)
ctx.SetTargetElementDebuff(PropertyType.Cold, 10)
ctx.printEnvironment()

weapon.setContext(ctx)
weapon.updateCurrentProperties()
weapon.printAllProperties()

all_permutations = getAllPermutations(ctx, 8)
# 随机打乱
import random
random.shuffle(all_permutations)
max_dps = 0
max_dps_permutation = None
import time
start_time = time.time()
for idx, perm in enumerate(all_permutations):
    ctx.target.clearElementDebuff()
    weapon.setCardPermutes(perm)
    weapon.updateCurrentProperties()
    currentDps = dps.CalculateAverageDPS(ctx)
    if currentDps > max_dps:
        max_dps = currentDps
        max_dps_permutation = perm
        print(f"新的最大DPS: {max_dps:.2f}，卡牌组合: {[card.name for card in perm]}")

    if idx % 1000 == 0:
        process = (idx / len(all_permutations)) * 100
        print(f"进度: {process:.2f}%")
end_time = time.time()
print(f"所有 {len(all_permutations)} 个排列已处理完毕。")
print(f'总耗时: {end_time - start_time:.2f}秒')
print(f"找到的最大DPS: {max_dps:.2f}")
print(f"最大DPS对应的卡牌组合: {[card.name for card in max_dps_permutation]}")
weapon.setCardPermutes(max_dps_permutation)
weapon.updateCurrentProperties()
weapon.printAllProperties()
OneHitDamage_Critical = dps.CalculateDamageOnce(ctx, forceCritical=1, forceTrigger=-1)
OneHitDamage_Uncritical = dps.CalculateDamageOnce(ctx, forceCritical=-1, forceTrigger=-1)
print(f"首发伤害（暴击）：{OneHitDamage_Critical:.2f}")
print(f"首发伤害（非暴击）：{OneHitDamage_Uncritical:.2f}")