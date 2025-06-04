from abc import ABC, abstractmethod
from enum import Enum, unique
import copy

@unique
class CardSet(Enum):
	Unset = 0
	Reverse = 1 # 逆转，每张卡加30%暴击
	Ghost = 2 # 鬼卡，元素转动能

@unique
class EnemyMaterial(Enum):
	Void = 0
	Mechanical = 1
	Biological = 2
	Energy = 3

@unique
class PropertyType(Enum):
	# 伤害类型
	Physics = 0
	Cold = 1
	Electric = 2
	Fire = 3
	Poison = 4
	# 复合伤害类型
	Cracking = 15
	Radiation = 16
	Gas = 17
	Magnetic = 18
	Ether = 19
	Virus = 20
	# 暴击
	CriticalChance = 100
	CriticalDamage = 101
	# 触发
	TriggerChance = 102
	# 攻击速度
	AttackSpeed = 103
	# 多重
	MultiStrike = 1001
	# 弱点伤害
	Headshot = 104
	# 异常持续时间
	DebuffDuration = 105
	# 弹容量
	MagazineSize = 1002
	# 装填时间
	ReloadTime = 1003
	# 穿甲率和穿甲值
	PenetrationRate = 106
	PenetrationValue = 107
	# 武器伤害
	AllDamage = 108
	
	# 是否是远程武器才有的参数
	def isRanged(self):
		return self.value > 1000 and self.value < 2000
	
	# 是否是可复合的基础伤害类属性
	def isBaseElementDamage(self):
		return self.value > 0 and self.value <= 4
	
	def isElementDamage(self):
		return self.value > 0 and self.value < 21
	
	def isDamage(self):
		return self.value <= 20
	
	def toString(self):
		if self in PropertyTypeToString:
			return PropertyTypeToString[self]
		else:
			raise ValueError(f"Unknown PropertyType: {self}")

PropertyTypeToString = {
	PropertyType.Physics: "动能",
	PropertyType.Cold: "冰冻",
	PropertyType.Electric: "赛能",
	PropertyType.Fire: "热波",
	PropertyType.Poison: "创生",
	PropertyType.Cracking: "裂化",
	PropertyType.Radiation: "辐射",
	PropertyType.Gas: "毒气",
	PropertyType.Magnetic: "磁暴",
	PropertyType.Ether: "以太",
	PropertyType.Virus: "病毒",
	PropertyType.CriticalChance: "暴击率",
	PropertyType.CriticalDamage: "暴击伤害",
	PropertyType.TriggerChance: "触发率",
	PropertyType.AttackSpeed: "攻击速度",
	PropertyType.MultiStrike: "多重打击",
	PropertyType.Headshot: "弱点伤害",
	PropertyType.DebuffDuration: "异常持续时间",
	PropertyType.MagazineSize: "弹容量",
	PropertyType.ReloadTime: "装填时间",
	PropertyType.PenetrationRate: "穿甲率",
	PropertyType.PenetrationValue: "穿甲值",
	PropertyType.AllDamage: "武器伤害"
}
	
Adjustment = [
	[1,		1,		1,		1], 	# Physics
	[1.25,	0.85,	1,		1], 	# Cold
	[1,		1,		0.75,	1.25], 	# Electric
	[0.85,	1.25,	1,		1], 	# Fire
	[1,		1,		1.25,	0.75], 	# Poison
	[1.5,	0.5,	1,		1.5], 	# Cracking
	[0.5,	1.5,	1,		1.75], 	# Radiation
	[1,		1,		1.75,	0.5], 	# Gas
	[1,		1.75,	0.5,	1.75], 	# Magnetic
	[1.75,	1,		0.5,	1], 	# Ether
	[0.5,	1,		1.5,	1], 	# Virus
]
def GetDamageAdjustment(propertyType: PropertyType, enemyMaterial: EnemyMaterial):
	return Adjustment[propertyType.value][enemyMaterial.value]

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

	def add(self, property, ignore_type_check=False):
		if not isinstance(property, Property):
			raise TypeError("Expected a Property instance")
		if not ignore_type_check and self.propertyType != property.propertyType:
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

	def __deepcopy__(self, memo):
		new_snapshot = PropertySnapshot([])
		for propertyType, property in self.datas.items():
			new_snapshot.datas[propertyType] = copy.deepcopy(property, memo)
		return new_snapshot
	
	# 各伤害合并的面板总伤害
	def getTotalDamage(self):
		totalDamage = 0.0
		for propertyType, property in self.datas.items():
			if propertyType.isDamage():
				totalDamage += property.get()
		return totalDamage
	
	def update(self, propertiesArray):
		baseDamage = self.getTotalDamage()
		# 先计算非元素伤害的属性
		elementDamageArray = []
		for property in propertiesArray:
			if property.propertyType.isBaseElementDamage():
				elementDamageArray.append(property)
			else:
				self.datas[property.propertyType].add(property)
		# 将元素伤害百分比转化为数值
		for property in elementDamageArray:
			if property.propertyType.isBaseElementDamage():
				property.value = property.addon * baseDamage / 100.0
				property.addon = 0.0
			else:
				raise ValueError("Invalid property type for element damage")
		# 将原先的元素伤害属性添加到elementDamageArray末尾，然后清空快照中的元素伤害属性
		for propertyType in PropertyType:
			if propertyType.isElementDamage() and self.datas[propertyType].get() != 0:
				elementDamageArray.append(copy.deepcopy(self.datas[propertyType]))
				self.datas[propertyType].clear()
		# 按顺序开始复合元素伤害：
		# 裂化 = 热波 + 冰冻
		# 辐射 = 赛能 + 创生
		# 以太 = 热波 + 赛能
		# 病毒 = 冰冻 + 创生
		# 磁暴 = 赛能 + 冰冻
		# 毒气 = 创生 + 热波
		# 如果一种基本元素加成多次出现，且之前出现的已经参与了伤害复合，那么后出现的加成会自动加入到前面的复合伤害当中
		FinalDamageArray = []
		def FindElementDamage(propertyType: PropertyType):
			for property in FinalDamageArray:
				if property.propertyType == propertyType:
					return True, property
			return False, None
		
		def FindElementDamageComposed(propertyType: PropertyType):
			property = None
			find = False
			if propertyType == PropertyType.Fire:
				find, property = FindElementDamage(PropertyType.Cracking)
				if not find:
					find, property = FindElementDamage(PropertyType.Radiation)
			elif propertyType == PropertyType.Cold:
				find, property = FindElementDamage(PropertyType.Radiation)
				if not find:
					find, property = FindElementDamage(PropertyType.Magnetic)
			elif propertyType == PropertyType.Electric:
				find, property = FindElementDamage(PropertyType.Cracking)
				if not find:
					find, property = FindElementDamage(PropertyType.Gas)
			elif propertyType == PropertyType.Poison:
				find, property = FindElementDamage(PropertyType.Gas)
				if not find:
					find, property = FindElementDamage(PropertyType.Magnetic)
			return find, property

		for i in range(len(elementDamageArray)):
			damageType = elementDamageArray[i].propertyType
			# 先检查是否有同类型的元素伤害已经存在
			find, property = FindElementDamage(damageType)
			if find:
				# 如果有，直接将当前元素伤害加到已有的元素伤害上
				property.add(elementDamageArray[i])
				continue
			# 如果没有，检查是否有该元素参与的复合元素伤害已经存在
			find, property = FindElementDamageComposed(damageType)
			if find:
				# 如果有，将当前元素伤害加到已有的复合元素伤害上
				property.add(elementDamageArray[i], ignore_type_check=True)
				continue
			# 如果没有，检查是否有可复合的元素伤害已经存在
			if damageType == PropertyType.Fire:
				# 热波
				find, property = FindElementDamage(PropertyType.Cold)
				if find:
					# 如果有冰冻，复合成裂化
					property.value += elementDamageArray[i].get()
					property.addon = 0.0
					property.propertyType = PropertyType.Cracking
					continue
				else:
					find, property = FindElementDamage(PropertyType.Electric)
					if find:
						# 如果有赛能，复合成辐射
						property.value += elementDamageArray[i].get()
						property.addon = 0.0
						property.propertyType = PropertyType.Radiation
						continue
					else:
						find, property = FindElementDamage(PropertyType.Poison)
						if find:
							# 如果有创生，复合成毒气
							property.value += elementDamageArray[i].get()
							property.addon = 0.0
							property.propertyType = PropertyType.Gas
							continue
			elif damageType == PropertyType.Cold:
				# 冰冻
				find, property = FindElementDamage(PropertyType.Electric)
				if find:
					# 如果有赛能，复合成辐射
					property.value += elementDamageArray[i].get()
					property.addon = 0.0
					property.propertyType = PropertyType.Radiation
					continue
				else:
					find, property = FindElementDamage(PropertyType.Poison)
					if find:
						# 如果有创生，复合成病毒
						property.value += elementDamageArray[i].get()
						property.addon = 0.0
						property.propertyType = PropertyType.Virus
						continue
					else:
						find, property = FindElementDamage(PropertyType.Fire)
						if find:
							# 如果有热波，复合成磁暴
							property.value += elementDamageArray[i].get()
							property.addon = 0.0
							property.propertyType = PropertyType.Magnetic
							continue
			elif damageType == PropertyType.Electric:
				# 赛能
				find, property = FindElementDamage(PropertyType.Fire)
				if find:
					# 如果有热波，复合成辐射
					property.value += elementDamageArray[i].get()
					property.addon = 0.0
					property.propertyType = PropertyType.Radiation
					continue
				else:
					find, property = FindElementDamage(PropertyType.Cold)
					if find:
						# 如果有冰冻，复合成磁暴
						property.value += elementDamageArray[i].get()
						property.addon = 0.0
						property.propertyType = PropertyType.Magnetic
						continue
					else:
						find, property = FindElementDamage(PropertyType.Poison)
						if find:
							# 如果有创生，复合成毒气
							property.value += elementDamageArray[i].get()
							property.addon = 0.0
							property.propertyType = PropertyType.Gas
							continue
			elif damageType == PropertyType.Poison:
				# 创生
				find, property = FindElementDamage(PropertyType.Electric)
				if find:
					# 如果有赛能，复合成辐射
					property.value += elementDamageArray[i].get()
					property.addon = 0.0
					property.propertyType = PropertyType.Radiation
					continue
				else:
					find, property = FindElementDamage(PropertyType.Fire)
					if find:
						# 如果有热波，复合成毒气
						property.value += elementDamageArray[i].get()
						property.addon = 0.0
						property.propertyType = PropertyType.Gas
						continue
					else:
						find, property = FindElementDamage(PropertyType.Cold)
						if find:
							# 如果有冰冻，复合成磁暴
							property.value += elementDamageArray[i].get()
							property.addon = 0.0
							property.propertyType = PropertyType.Magnetic
							continue
			# 如果没有可复合的元素伤害，直接添加到FinalDamageArray
			FinalDamageArray.append(copy.deepcopy(elementDamageArray[i]))
		
		# 将FinalDamageArray中的元素伤害进行AllDamage的加成
		for property in FinalDamageArray:
			property.value = property.value * (1 + self.datas[PropertyType.AllDamage].addon / 100.0)

		# 最后将FinalDamageArray中的元素伤害添加到快照中
		for property in FinalDamageArray:
			if property.propertyType.isElementDamage():
				self.datas[property.propertyType].add(property, ignore_type_check=True)
			else:
				raise ValueError("Invalid property type for element damage")


	def update_ghost(self, propertiesArray):
		# 魈鬼系列应用另一套伤害公式
		# 目前先不实现
		pass


# 所有卡牌的基类
class CardBase:
	def __init__(self, name, weaponType: WeaponType = None):
		self.name = name
		self.weaponType = weaponType

	@abstractmethod
	def getProperties(self):
		pass

class CardCommon(CardBase):
	# 常规卡牌，只有一条属性
	def __init__(self, name, property: Property, weaponType: WeaponType = None, cardSet: CardSet = CardSet.Unset):
		super().__init__(name, weaponType)
		self.property = property
		self.cardSet = CardSet

	def getProperties(self):
		return [self.property]

class CardRaven(CardBase):
	# 紫卡，可拥有多条属性
	def __init__(self, name, properties : list, WeaponType: WeaponType = None):
		super().__init__(name, WeaponType)
		self.properties = properties

	def getProperties(self):
		return self.properties

# 所有武器的基类
class WeaponBase:
	def __init__(self, name, baseProperties : PropertySnapshot):
		self.name = name
		self.baseProperties = baseProperties
		self.currentProperties = None
		self.cards = [None, None, None, None, None, None, None, None]  # 最多8张卡牌

	# 安装卡牌
	def setCardAtIndex(self, index, card : CardBase):
		if index < 0 or index >= 8:
			raise IndexError("Index out of range")
		self.cards[index] = card
		
	def getCardAtIndex(self, index):
		if index < 0 or index >= 8:
			raise IndexError("Index out of range")
		return self.cards[index]
	
	def updateCurrentProperties(self):
		self.currentProperties = copy.deepcopy(self.baseProperties)
		HasGhostCard = False
		for card in self.cards:
			if isinstance(card, CardCommon) and card.cardSet == CardSet.Ghost:
				HasGhostCard = True
		if HasGhostCard:
			# 魈鬼系列应用另一套伤害公式
			pass
		else:
			propertyArray = []
			for card in self.cards:
				if card is not None:
					propertyArray.extend(card.getProperties())
			self.currentProperties.update(propertyArray)

	def printAllProperties(self):
		if self.currentProperties is None:
			self.updateCurrentProperties()
		print(f"Weapon: {self.name}")
		print(f"Total Damage: {self.currentProperties.getTotalDamage()}")
		for propertyType, property in self.currentProperties.datas.items():
			if property.get() != 0:
				print(f"{propertyType.toString()}: {property.get()} (Value: {property.value}, Addon: {property.addon})")
		print("Cards:")
		for card in self.cards:
			if card is not None:
				print(f"- {card.name} ({card.weaponType})")


