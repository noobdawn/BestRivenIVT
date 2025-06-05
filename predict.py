from core import *
from cards import *
import dps
from env import env
import weapons

env.SetNum[CardSet.Ghost.value] = 2  # 魈鬼之眼套装数量
env.SetNum[CardSet.Reverse.value] = 2  # 逆转之心套装数量
env.useNianSkill = False  # 使用年春秋技能
env.nianSkillStrength = 200
env.invasionAuraNum = 1  # 侵犯光环数量
print("当前环境:")
env.printEnvironment()

enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
enemy.armor = 850

                  
waterdrop_prime = weapons.WaterDrop_Prime()
waterdrop_prime.setCardAtIndex(0, getRifleCards("魈鬼之眼"))
waterdrop_prime.setCardAtIndex(1, getRifleCards("增压枪膛"))
waterdrop_prime.setCardAtIndex(2, CardRiven("水滴 多重（裂罅）", 
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
waterdrop_prime.printAllProperties()

dps_in_magazine = dps.CalculateAverageDPS(waterdrop_prime, enemy, env)
print(f"{waterdrop_prime.name} 平均DPS: {dps_in_magazine:.2f}")