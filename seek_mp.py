from data.env import *
import data.cards as cards
import data.weapons as weapons
import data.armors as armors
from core.permutations import getAllPermutations
import core.dps as dps
import multiprocessing
from tqdm import tqdm
import time

def calculate_dps_for_permutation(perm):
    """
    为单个卡牌组合计算DPS。此函数将在单独的进程中运行。
    """
    # 为每个进程重新创建对象，以避免跨进程共享状态的问题
    weapon = weapons.IceFall_Prime()
    armor = armors.Yinniaoguilin()
    ctx = Context(armor, weapon)

    # 应用基础设置
    ctx.SetCardSetNum(CardSet.Invasion, 2)
    ctx.SetCharacterSkillStrength(200)
    ctx.SetTargetSkillDebuff(SkillFlag.Qianyinfeidan, True)
    ctx.SetTargetElementDebuff(PropertyType.Cold, 10)
    
    weapon.setContext(ctx)

    # 应用当前排列并计算DPS
    ctx.target.clearElementDebuff()
    weapon.setCardPermutes(perm)
    weapon.updateCurrentProperties()
    currentDps = dps.CalculateAverageDPS(ctx)
    
    return currentDps, perm

def main():
    # 原始设置
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
    
    max_dps = 0
    max_dps_permutation = None
    
    start_time = time.time()

    # 使用多进程池
    num_processes = multiprocessing.cpu_count()
    print(f"使用 {num_processes} 个进程进行计算...")
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        # 使用tqdm来跟踪进度
        results = list(tqdm(pool.imap_unordered(calculate_dps_for_permutation, all_permutations), total=len(all_permutations), desc="计算DPS"))

    # 从结果中找到最大值
    for currentDps, perm in results:
        if currentDps > max_dps:
            max_dps = currentDps
            max_dps_permutation = perm

    end_time = time.time()
    
    print(f"\n所有 {len(all_permutations)} 个排列已处理完毕。")
    print(f'总耗时: {end_time - start_time:.2f}秒')
    print(f"找到的最大DPS: {max_dps:.2f}")
    print(f"最大DPS对应的卡牌组合: {[card.name for card in max_dps_permutation]}")
    
    # 使用找到的最佳组合更新并打印最终属性和伤害
    weapon.setCardPermutes(max_dps_permutation)
    weapon.updateCurrentProperties()
    weapon.printAllProperties()
    OneHitDamage_Critical = dps.CalculateDamageOnce(ctx, forceCritical=1, forceTrigger=-1)
    OneHitDamage_Uncritical = dps.CalculateDamageOnce(ctx, forceCritical=-1, forceTrigger=-1)
    print(f"首发伤害（暴击）：{OneHitDamage_Critical:.2f}")
    print(f"首发伤害（非暴击）：{OneHitDamage_Uncritical:.2f}")

if __name__ == "__main__":
    main()