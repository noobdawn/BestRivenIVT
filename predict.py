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
print("")

enemy = EnemyBase("测试敌人", 0, EnemyMaterial.Mechanical)
enemy.armor = 850
enemy.setConstantDebuff(PropertyType.Virus, 10)  # 设置易伤病毒层数为10
print("当前敌人:")
enemy.printEnemyInfo()
print("")
                  
waterdrop_prime = weapons.WaterDrop_Prime()
waterdrop_prime.setCardAtIndex(0, getCardByName("魈鬼之眼", WeaponType.Rifle))
waterdrop_prime.setCardAtIndex(1, getCardByName("增压枪膛", WeaponType.Rifle))
waterdrop_prime.setCardAtIndex(2, CardRiven("水滴 多重（裂罅）", 
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
waterdrop_prime.printAllProperties()

dps_in_magazine = dps.CalculateAverageDPS(waterdrop_prime, enemy, env)
print(f"{waterdrop_prime.name} 平均DPS: {dps_in_magazine:.2f}")