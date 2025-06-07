# 单元测试，用于测试各种情况
import unittest
from core.baseclass import *
from data.env import env
from data.cards import *
import data.weapons
import core.dps

class TestDPSCalculation(unittest.TestCase):

    # 测试DoT伤害用例1
    # 用例：默认环境，私法大角星，上一张火元素
    # 伤害结果：37 ± 1
    def test_DoT_0(self):
        env.reset()
        
        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        weapon = data.weapons.Arcturus_Primer()
        weapon.setCardAtIndex(0, getCardByName("高温枪管", WeaponType.Rifle))
        weapon.updateCurrentProperties()

        # 计算触发元素异常后每层裂化DoT的伤害
        baseWeaponDamage = core.dps.GetBaseWeaponDamage(weapon)
        externalDamageMultiplier = core.dps.GetExternalDamageMultiplier(weapon, enemy, env)
        uncriticalMultiplier, criticalMultiplier = core.dps.GetCriticalMultiplier(weapon, enemy)
        debuffProperty = core.dps.TriggerElementDebuff(baseWeaponDamage)
        DoTMultiplier = 0.0
        if debuffProperty == PropertyType.Fire or debuffProperty == PropertyType.Electric or debuffProperty == PropertyType.Gas:
            # 热波、赛能、毒气元素异常的持续伤害倍率为 0.5，持续6秒
            DoTMultiplier = 0.5
        elif debuffProperty == PropertyType.Cracking:
            # 裂化的伤害倍率为 0.35，持续6秒
            DoTMultiplier = 0.35
        if DoTMultiplier > 0:
            DoTDamage = baseWeaponDamage.sum() * externalDamageMultiplier * uncriticalMultiplier * DoTMultiplier
            DoTDamageTaken = core.dps.DamageTakenDoT(DoTDamage, debuffProperty, enemy)

            self.assertFalse(debuffProperty != PropertyType.Cracking, "元素触发异常，预期为裂化元素异常，实际为" + debuffProperty.toString())
            self.assertAlmostEqual(DoTDamageTaken, 37, delta=1, msg="DoT伤害计算错误，预期为37 ± 1")
        else:
            self.fail("元素触发异常，预期为裂化元素异常")

    # 测试DoT伤害用例2
    # 用例：默认环境，聚焦矿灯，上多重点射、逆转之心、长枪专家、裸露铅心、快速回膛
    # 伤害结果：电元素异常触发，伤害为 5；裂化元素异常触发，伤害为 7
    # 电层数和裂化层数之比约为10:9
    def test_DoT_1(self):
        env.reset()
        
        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        weapon = data.weapons.FocusLamp()
        weapon.setCardAtIndex(0, getCardByName("多重点射", WeaponType.Rifle))
        weapon.setCardAtIndex(1, getCardByName("逆转之心", WeaponType.Rifle))
        weapon.setCardAtIndex(2, getCardByName("长枪专家", WeaponType.Rifle))
        weapon.setCardAtIndex(3, getCardByName("裸露铅心", WeaponType.Rifle))
        weapon.setCardAtIndex(4, getCardByName("快速回膛", WeaponType.Rifle))
        weapon.updateCurrentProperties()

        # 计算触发元素异常后每层电元素异常和裂化DoT的伤害
        baseWeaponDamage = core.dps.GetBaseWeaponDamage(weapon)
        externalDamageMultiplier = core.dps.GetExternalDamageMultiplier(weapon, enemy, env)
        uncriticalMultiplier, criticalMultiplier = core.dps.GetCriticalMultiplier(weapon, enemy)
        
        electricCount = 0
        crackingCount = 0
        # 重复1000次触发元素异常，统计电元素异常和裂化的层数
        for _ in range(1000):
            debuffProperty = core.dps.TriggerElementDebuff(baseWeaponDamage)
            if debuffProperty == PropertyType.Electric:
                electricCount += 1
            elif debuffProperty == PropertyType.Cracking:
                crackingCount += 1
            else:
                self.fail("元素触发异常，预期为电或裂化元素异常，实际为" + debuffProperty.toString())

        # 计算每层电元素异常和裂化DoT的伤害
        electricDoTDamage = baseWeaponDamage.sum() * externalDamageMultiplier * uncriticalMultiplier * 0.5
        crackingDoTDamage = baseWeaponDamage.sum() * externalDamageMultiplier * uncriticalMultiplier * 0.35
        electricDoTDamageTaken = core.dps.DamageTakenDoT(electricDoTDamage, PropertyType.Electric, enemy)
        crackingDoTDamageTaken = core.dps.DamageTakenDoT(crackingDoTDamage, PropertyType.Cracking, enemy)
        self.assertAlmostEqual(electricDoTDamageTaken, 5, delta=1, msg="电元素异常DoT伤害计算错误，预期为5 ± 1")
        self.assertAlmostEqual(crackingDoTDamageTaken, 7, delta=1, msg="裂化元素异常DoT伤害计算错误，预期为7 ± 1")

    # 测试DoT伤害用例3
    # 用例：默认环境，私法大角星，上一张火元素
    # 伤害结果：需触发裂化元素异常，伤害总量为31 + 37 * 6 = 253
    def test_DoT_2(self):
        env.reset()
        
        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        weapon = data.weapons.Arcturus_Primer()
        weapon.setCardAtIndex(0, getCardByName("高温枪管", WeaponType.Rifle))
        weapon.updateCurrentProperties()

        damageTaken = core.dps.CalculateDamageOnce(weapon, enemy, env, forceCritical=-1, forceTrigger=1)
        self.assertAlmostEqual(damageTaken, 253, delta=1, msg="DoT伤害计算错误，预期为253 ± 1")

    # 测试直接伤害用例1
    # 单发伤害为1159~1170之间
    def test_DirectDamage_0(self):
        env.reset()
        env.SetNum[CardSet.Ghost.value] = 0  # 魈鬼之眼套装数量
        env.SetNum[CardSet.Reverse.value] = 2  # 逆转之心套装数量
        env.SetNum[CardSet.Invasion.value] = 1  # 侵犯光环数量

        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        weapon = data.weapons.WaterDrop_Prime()
        weapon.setCardAtIndex(0, getCardByName("零度弹头", WeaponType.Rifle))
        weapon.setCardAtIndex(1, getCardByName("弹孔注射", WeaponType.Rifle))
        weapon.setCardAtIndex(2, getCardByName("高温枪管", WeaponType.Rifle))
        weapon.setCardAtIndex(3, getCardByName("增压枪膛", WeaponType.Rifle))
        weapon.setCardAtIndex(4, getCardByName("扩容弹匣", WeaponType.Rifle))
        weapon.setCardAtIndex(5, getCardByName("裸露铅心", WeaponType.Rifle))
        weapon.setCardAtIndex(6, getCardByName("弹道修正", WeaponType.Rifle))
        weapon.setCardAtIndex(7, CardRiven("水滴 多重（裂罅）", 
            [
                Property(PropertyType.MultiStrike, 0, 104),
                Property(PropertyType.AllDamage, 0, 204),
            ], 
            WeaponType.Rifle))
        weapon.updateCurrentProperties()
        OneHitDamage = core.dps.CalculateDamageOnce(weapon, enemy, env, forceCritical=True, forceTrigger=-1)
        self.assertAlmostEqual(OneHitDamage, 1165, delta=5, msg="单发伤害计算错误，预期为1159~1170之间")

    # 测试直接伤害用例2
    # 主要测试带鬼卡的伤害
    # 单发伤害为 2012~2048 之间
    def test_DirectDamage_1(self):
        env.reset()
        env.SetNum[CardSet.Ghost.value] = 2  # 魈鬼之眼套装数量
        env.SetNum[CardSet.Reverse.value] = 2  # 逆转之心套装数量
        env.SetNum[CardSet.Invasion.value] = 1  # 侵犯光环数量

        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        weapon = data.weapons.WaterDrop_Prime()
        weapon.setCardAtIndex(0, getCardByName("零度弹头", WeaponType.Rifle))
        weapon.setCardAtIndex(1, getCardByName("魈鬼之眼", WeaponType.Rifle))
        weapon.setCardAtIndex(2, getCardByName("多重点射", WeaponType.Rifle))
        weapon.setCardAtIndex(3, getCardByName("增压枪膛", WeaponType.Rifle))
        weapon.setCardAtIndex(4, getCardByName("快速回膛", WeaponType.Rifle))
        weapon.setCardAtIndex(5, getCardByName("裸露铅心", WeaponType.Rifle))
        weapon.setCardAtIndex(6, getCardByName("弹道修正", WeaponType.Rifle))
        weapon.setCardAtIndex(7, CardRiven("水滴 多重（裂罅）", 
            [
                Property(PropertyType.MultiStrike, 0, 104),
                Property(PropertyType.AllDamage, 0, 204),
            ], 
            WeaponType.Rifle))
        weapon.updateCurrentProperties()
        OneHitDamage = core.dps.CalculateDamageOnce(weapon, enemy, env, forceCritical=True, forceTrigger=-1)
        self.assertAlmostEqual(OneHitDamage, 2030, delta=18, msg="单发伤害计算错误，预期为2012~2048之间")

if __name__ == '__main__':
    unittest.main()