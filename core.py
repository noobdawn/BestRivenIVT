from abc import ABC, abstractmethod
from enum import Enum, unique

@unique
class PropertyType(Enum):
    # 伤害类型
    Physics = 0,
    Cold = 1,
    Electric = 2,
    Fire = 3,
    Poison = 4,
    # 复合伤害类型
    Cracking = 15,
    Radiation = 16,
    Gas = 17,
    Magnetic = 18,
    Ether = 19,
    Virus = 20,
    # 面板伤害
    AllDamage = 21,
    # 暴击
    CriticalChance = 100,
    CriticalDamage = 101,
    # 触发
    TriggerChance = 102
    # 攻击速度
    AttackSpeed = 103,
    # 多重
    MultiStrike = 1001,
    # 弱点伤害
    Headshot = 104,
    # 异常持续时间
    DebuffDuration = 105,
    # 弹容量
    MagazineSize = 1002,
    # 装填时间
    ReloadTime = 1003,
    # 穿甲率和穿甲值
    PenetrationRate = 106,
    PenetrationValue = 107,


    # 是否是近战武器才有的参数
    def isMelee(self):
        return self > 2000 and self < 3000
    
    # 是否是远程武器才有的参数
    def isRanged(self):
        return self > 1000 and self < 2000

@unique
class WeaponType(Enum):
    Shotgun = 0
    Rifle = 1
    MachineGun = 2
    Laser = 3
    RocketLauncher = 4
    Melee = 5
    Pistol = 6
    SubmachineGun = 7
    Sniper = 8

class Property:
    def __init__(self, propertyType: PropertyType, value: float = 0.0, addon: float = 0.0, from_mod=False):
        self.propertyType = propertyType
        self.value = value
        self.addon = addon
        self.from_mod = from_mod

    def get(self):
        return self.value * (1 + self.addon / 100.0)
    
    def clear(self):
        self.value = 0.0
        self.addon = 0.0

    def add(self, property):
        if not isinstance(property, Property):
            raise TypeError("Expected a Property instance")
        if self.propertyType != property.propertyType:
            raise ValueError("Property types do not match")
        if property.value * property.addon != 0:
            raise ValueError("Property value and addon should not both be non-zero")
        self.value += property.value
        self.addon += property.addon

    @classmethod
    def createCardProperty(cls, propertyType: PropertyType, addon: float = 0.0):
        return cls(propertyType, 0.0, addon, from_mod=True)


class PropertySnapshot:
    def __init__(self, properties):
        self.datas = {}
        for propertyType in PropertyType:
            self.datas[propertyType] = Property(propertyType)
        for property in properties:
            self.datas[property.propertyType].add(property)


# 所有卡牌的基类
class CardBase:
    def __init__(self, name, WeaponType: WeaponType = None):
        self.name = name
        self.weaponType = WeaponType

    @abstractmethod
    def getPropertys(self):
        pass

class CardCommon(CardBase):
    # 常规卡牌，只有一条属性
    def __init__(self, name, property: Property, WeaponType: WeaponType = None):
        super().__init__(name, WeaponType)
        self.property = property

    def getPropertys(self):
        return [self.property]

class CardRaven(CardBase):
    # 紫卡，可拥有多条属性
    def __init__(self, name, properties: list[Property], WeaponType: WeaponType = None):
        super().__init__(name, WeaponType)
        self.properties = properties

    def getPropertys(self):
        return self.properties

# 所有武器的基类
class WeaponBase:
    def __init__(self, name, baseProperties : PropertySnapshot):
        self.name = name
        self.baseProperties = baseProperties
        self.currentProperties = PropertySnapshot([])
        self.cards = []

    # 安装和移除卡牌
    def setCardAtIndex(self, index, card : CardBase):
        if index < 0 or index >= len(self.cards):
            raise IndexError("Index out of range")
        self.cards[index] = card

    def removeCardAtIndex(self, index):
        if index < 0 or index >= 8:
            raise IndexError("Index out of range")
        self.cards[index] = None

    def getCardAtIndex(self, index):
        if index < 0 or index >= len(self.cards):
            raise IndexError("Index out of range")
        return self.cards[index]
