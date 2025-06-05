# 测试单元，用于测试各种情况

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
        env.useNianSkill = False  # 使用年春秋技能
        env.nianSkillStrength = 200
        env.invasionAuraNum = 1  # 侵犯光环数量

        enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
        enemy.armor = 850

        waterdrop_prime = weapons.WaterDrop_Prime()
        waterdrop_prime.setCardAtIndex(0, getRifleCards("魈鬼之眼"))
        waterdrop_prime.setCardAtIndex(1, getRifleCards("增压枪膛"))
        waterdrop_prime.setCardAtIndex(2, CardRiven("水滴", 
            [
                Property(PropertyType.MultiStrike, 0, 104),
                Property(PropertyType.AllDamage, 0, 204)
            ], 
            WeaponType.Rifle))
        waterdrop_prime.setCardAtIndex(3, getRifleCards("多重点射"))
        waterdrop_prime.setCardAtIndex(4, getRifleCards("逆转之心"))
        waterdrop_prime.setCardAtIndex(5, getRifleCards("致密打击"))
        waterdrop_prime.setCardAtIndex(6, getRifleCards("弹道修正"))
        waterdrop_prime.setCardAtIndex(7, getRifleCards("裸露铅心"))
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
        
unittest.main()