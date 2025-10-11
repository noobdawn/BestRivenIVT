# 记录了各个装甲的数据，以30级为标准

from core.baseclass import *

class Shouzhanqibing(ArmorBase):
    def __init__(self):
        super().__init__(ArmorSet.Shouzhanqibing, SubWeaponType.AssaultRifle)
        self.properties[CharacterPropertyType.Health.value].set(650.0, 0)
        self.properties[CharacterPropertyType.Shield.value].set(300.0, 0)
        self.properties[CharacterPropertyType.Energy.value].set(150.0, 0)
        self.properties[CharacterPropertyType.Armor.value].set(600.0, 0)
        self.properties[CharacterPropertyType.DamageReduction.value].set(100, 0)
        self.properties[CharacterPropertyType.SkillStrength.value].set(100.0, 0)
        self.properties[CharacterPropertyType.SkillRange.value].set(100.0, 0)
        self.properties[CharacterPropertyType.SkillCost.value].set(100.0, 0)
        self.properties[CharacterPropertyType.SkillDuration.value].set(100.0, 0)
        self.properties[CharacterPropertyType.MoveSpeed.value].set(1.44, 0)
        self.properties[CharacterPropertyType.ShieldRechargeRate.value].set(100.0, 0)
        self.properties[CharacterPropertyType.ShieldRechargeDelay.value].set(100.0, 0)

class Yinniaoguilin(ArmorBase):
    def __init__(self):
        super().__init__(ArmorSet.Yinniaoguilin, SubWeaponType.Shotgun)
        self.properties[CharacterPropertyType.Health.value].set(650.0, 0)
        self.properties[CharacterPropertyType.Shield.value].set(300.0, 0)
        self.properties[CharacterPropertyType.Energy.value].set(150.0, 0)
        self.properties[CharacterPropertyType.Armor.value].set(600.0, 0)
        self.properties[CharacterPropertyType.DamageReduction.value].set(100, 0)
        self.properties[CharacterPropertyType.SkillStrength.value].set(100.0, 0)
        self.properties[CharacterPropertyType.SkillRange.value].set(100.0, 0)
        self.properties[CharacterPropertyType.SkillCost.value].set(100.0, 0)
        self.properties[CharacterPropertyType.SkillDuration.value].set(100.0, 0)
        self.properties[CharacterPropertyType.MoveSpeed.value].set(1.44, 0)
        self.properties[CharacterPropertyType.ShieldRechargeRate.value].set(100.0, 0)
        self.properties[CharacterPropertyType.ShieldRechargeDelay.value].set(100.0, 0)
