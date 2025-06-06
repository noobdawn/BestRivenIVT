# 单元测试，用于测试各种情况
import unittest
from dps import *
from core import *
from env import env
from cards import *
import weapons
import dps

class TestDPSCalculation(unittest.TestCase):

    # 测试DoT伤害用例1
    # 用例：默认环境，私法大角星，上一张火元素
    # 伤害结果：37 ± 1
    def test_DoT_0(self):
        env.reset()
        
        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        weapon = weapons.Arcturus_Primer()
        weapon.setCardAtIndex(0, getCardByName("高温枪管", WeaponType.Rifle))
        weapon.updateCurrentProperties()

        # 计算触发元素异常后每层裂化DoT的伤害
        baseWeaponDamage = dps.GetBaseWeaponDamage(weapon)
        externalDamageMultiplier = dps.GetExternalDamageMultiplier(weapon, enemy, env)
        uncriticalMultiplier, criticalMultiplier = dps.GetCriticalMultiplier(weapon, enemy)
        debuffProperty = TriggerElementDebuff(baseWeaponDamage)
        DoTMultiplier = 0.0
        if debuffProperty == PropertyType.Fire or debuffProperty == PropertyType.Electric or debuffProperty == PropertyType.Gas:
            # 热波、赛能、毒气元素异常的持续伤害倍率为 0.5，持续6秒
            DoTMultiplier = 0.5
        elif debuffProperty == PropertyType.Cracking:
            # 裂化的伤害倍率为 0.35，持续6秒
            DoTMultiplier = 0.35
        if DoTMultiplier > 0:
            DoTDamage = baseWeaponDamage.sum() * externalDamageMultiplier * uncriticalMultiplier * DoTMultiplier
            DoTDamageTaken = dps.DamageTakenDoT(DoTDamage, debuffProperty, enemy)

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

        weapon = weapons.FocusLamp()
        weapon.setCardAtIndex(0, getCardByName("多重点射", WeaponType.Rifle))
        weapon.setCardAtIndex(1, getCardByName("逆转之心", WeaponType.Rifle))
        weapon.setCardAtIndex(2, getCardByName("长枪专家", WeaponType.Rifle))
        weapon.setCardAtIndex(3, getCardByName("裸露铅心", WeaponType.Rifle))
        weapon.setCardAtIndex(4, getCardByName("快速回膛", WeaponType.Rifle))
        weapon.printAllProperties()

        # 计算触发元素异常后每层电元素异常和裂化DoT的伤害
        baseWeaponDamage = dps.GetBaseWeaponDamage(weapon)
        externalDamageMultiplier = dps.GetExternalDamageMultiplier(weapon, enemy, env)
        uncriticalMultiplier, criticalMultiplier = dps.GetCriticalMultiplier(weapon, enemy)
        
        electricCount = 0
        crackingCount = 0
        # 重复1000次触发元素异常，统计电元素异常和裂化的层数
        for _ in range(1000):
            debuffProperty = TriggerElementDebuff(baseWeaponDamage)
            if debuffProperty == PropertyType.Electric:
                electricCount += 1
            elif debuffProperty == PropertyType.Cracking:
                crackingCount += 1
            else:
                self.fail("元素触发异常，预期为电或裂化元素异常，实际为" + debuffProperty.toString())

        # 计算每层电元素异常和裂化DoT的伤害
        electricDoTDamage = baseWeaponDamage.sum() * externalDamageMultiplier * uncriticalMultiplier * 0.5
        crackingDoTDamage = baseWeaponDamage.sum() * externalDamageMultiplier * uncriticalMultiplier * 0.35
        electricDoTDamageTaken = dps.DamageTakenDoT(electricDoTDamage, PropertyType.Electric, enemy)
        crackingDoTDamageTaken = dps.DamageTakenDoT(crackingDoTDamage, PropertyType.Cracking, enemy)
        self.assertAlmostEqual(electricDoTDamageTaken, 5, delta=1, msg="电元素异常DoT伤害计算错误，预期为5 ± 1")
        self.assertAlmostEqual(crackingDoTDamageTaken, 7, delta=1, msg="裂化元素异常DoT伤害计算错误，预期为7 ± 1")

if __name__ == '__main__':
    unittest.main()