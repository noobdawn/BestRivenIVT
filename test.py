# 单元测试，用于测试各种情况
import unittest
from dps import *
from core import *
from env import env
from cards import *
import weapons
import dps

class TestWeakArmor(unittest.TestCase):
    def test_waterdrop_prime(self):
        '''
        测试私法水滴使用魈鬼之眼套装和逆转之心套装的情况
        测试结果应为1526.90（暴击）或399.19（非暴击）
        '''
        env.reset()
        env.SetNum[CardSet.Ghost.value] = 2  # 魈鬼之眼套装数量
        env.SetNum[CardSet.Reverse.value] = 2  # 逆转之心套装数量
        env.invasionAuraNum = 1  # 侵犯光环数量

        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        waterdrop_prime = weapons.WaterDrop_Prime()
        waterdrop_prime.setCardAtIndex(0, getCardByName("魈鬼之眼", WeaponType.Rifle))
        waterdrop_prime.setCardAtIndex(1, getCardByName("增压枪膛", WeaponType.Rifle))
        waterdrop_prime.setCardAtIndex(2, CardRiven("水滴", 
            [
                Property(PropertyType.MultiStrike, 0, 104),
                Property(PropertyType.AllDamage, 0, 204)
            ], 
            WeaponType.Rifle))
        waterdrop_prime.setCardAtIndex(3, getCardByName("多重点射", WeaponType.Rifle))
        waterdrop_prime.setCardAtIndex(4, getCardByName("逆转之心", WeaponType.Rifle))
        waterdrop_prime.setCardAtIndex(5, getCardByName("致密打击", WeaponType.Rifle))
        waterdrop_prime.setCardAtIndex(6, getCardByName("弹道修正", WeaponType.Rifle))
        waterdrop_prime.setCardAtIndex(7, getCardByName("裸露铅心", WeaponType.Rifle))
        waterdrop_prime.updateCurrentProperties()

        damage, damageTimes, criticalLevel = dps.PullTriggerOnce(waterdrop_prime, enemy, env)
        damageTaken = dps.DamageTaken(damage, enemy)
        if criticalLevel == 1:
            # 如果不约等于 1526.90，则测试失败
            self.assertAlmostEqual(damageTaken, 1526.90, places=2)
        elif criticalLevel == 0:
            # 如果不约等于 399.19，则测试失败
            self.assertAlmostEqual(damageTaken, 199.19, places=2)
        else:
            # 能触发更高的暴击等级就是不正确的
            self.fail(f"Unexpected critical level: {criticalLevel}")
        
    def test_arcturus_primer(self):
        '''
        测试私法大角星的情况
        测试结果应为600（暴击）
        '''
        env.reset()

        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        arcturus_primer = weapons.Arcturus_Primer()
        arcturus_primer.setCardAtIndex(0, getCardByName("多重点射", WeaponType.Rifle))
        arcturus_primer.setCardAtIndex(1, getCardByName("弹孔注射", WeaponType.Rifle))
        arcturus_primer.setCardAtIndex(2, getCardByName("长枪专家", WeaponType.Rifle))
        arcturus_primer.setCardAtIndex(3, getCardByName("逆转之心", WeaponType.Rifle))
        arcturus_primer.setCardAtIndex(4, getCardByName("弹道修正", WeaponType.Rifle))
        arcturus_primer.setCardAtIndex(5, getCardByName("裸露铅心", WeaponType.Rifle))
        arcturus_primer.setCardAtIndex(7, getCardByName("增压枪膛", WeaponType.Rifle))
        arcturus_primer.updateCurrentProperties()

        criticalLevel = 0
        while criticalLevel != 1:
            # 触发一次攻击
            damage, damageTimes, criticalLevel = dps.PullTriggerOnce(arcturus_primer, enemy, env)
        damageTaken = dps.DamageTaken(damage, enemy)
        # 暴击伤害约等于 600，则测试失败
        self.assertAlmostEqual(damageTaken, 600, delta=2)
        
unittest.main()