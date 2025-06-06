from abc import ABC, abstractmethod
import numpy as np
import copy
from env import env
from ivtenum import *

# 128个介于0~1之间的随机数
_SEED = 114514.1919810
_RANDOM_NUMBERS = []
for i in range(128):
	_SEED = (_SEED * 16807) % 2147483647
	_RANDOM_NUMBERS.append(_SEED / 2147483647.0)
# 获取随机数
_RANDOM_INDEX = 0
def rand():
	'''
	获取一个介于0~1之间的随机数
	'''
	global _RANDOM_INDEX
	if _RANDOM_INDEX >= len(_RANDOM_NUMBERS):
		_RANDOM_INDEX = 0
	value = _RANDOM_NUMBERS[_RANDOM_INDEX]
	_RANDOM_INDEX += 1
	return value

# 伤害的组合体，实际上是一个由11个float组成的Numpy数组
class DamageCollection:
	def __init__(self, physics=0.0, cold=0.0, electric=0.0, fire=0.0, poison=0.0,
				 cracking=0.0, radiation=0.0, gas=0.0, magnetic=0.0, ether=0.0, virus=0.0):
		self.np_damage = np.array([
			physics, cold, electric, fire, poison,
			cracking, radiation, gas, magnetic, ether, virus
		], dtype=np.float32)

	def sum(self):
		'''
		返回所有伤害的总和
		'''
		return self.np_damage.sum()

	@classmethod
	def createDamage(cls, array : list):
		if len(array) != 11:
			raise ValueError("Array must have exactly 11 elements")
		return cls(*array)
	
	# 重载运算符
	# 核心运算逻辑
	def _element_wise_op(self, other, op):
		if isinstance(other, DamageCollection):
			new_array = op(self.np_damage, other.np_damage)
		elif isinstance(other, (int, float)):
			new_array = op(self.np_damage, other)
		else:
			return NotImplemented
		return DamageCollection(*new_array.tolist())

	# 运算符重载
	def __add__(self, other):
		return self._element_wise_op(other, np.add)
	
	def __sub__(self, other):
		return self._element_wise_op(other, np.subtract)
	
	def __mul__(self, other):
		return self._element_wise_op(other, np.multiply)
	
	def __truediv__(self, other):
		return self._element_wise_op(other, np.divide)
	
	# 反向运算符（处理标量在左侧的情况）
	__radd__ = __add__
	__rmul__ = __mul__
	
	def __rsub__(self, other):
		return DamageCollection(*other).__sub__(self)
	
	def __rtruediv__(self, other):
		return DamageCollection(*other).__truediv__(self)

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
		self.damageSnapshot = None
		self.update([])

	def __deepcopy__(self, memo):
		new_snapshot = PropertySnapshot([])
		for propertyType, property in self.datas.items():
			new_snapshot.datas[propertyType] = copy.deepcopy(property, memo)
		new_snapshot.update([])  # 确保快照是最新的
		return new_snapshot
	
	# 各伤害合并的面板总伤害
	def getTotalDamage(self):
		if self.damageSnapshot is None:
			self.damageSnapshot = DamageCollection.createDamage([
				self.datas[PropertyType.Physics].get(),
				self.datas[PropertyType.Cold].get(),
				self.datas[PropertyType.Electric].get(),
				self.datas[PropertyType.Fire].get(),
				self.datas[PropertyType.Poison].get(),
				self.datas[PropertyType.Cracking].get(),
				self.datas[PropertyType.Radiation].get(),
				self.datas[PropertyType.Gas].get(),
				self.datas[PropertyType.Magnetic].get(),
				self.datas[PropertyType.Ether].get(),
				self.datas[PropertyType.Virus].get()
			])
		return self.damageSnapshot.np_damage.sum()
	
	def getTriggerChance(self):
		'''获取触发几率'''
		triggerChance = self.datas[PropertyType.TriggerChance].get()
		return triggerChance
	
	def getCriticalChance(self):
		'''获取暴击率'''
		criticalChance = self.datas[PropertyType.CriticalChance].get()
		return criticalChance
	
	def getCriticalDamage(self):
		'''获取暴击伤害'''
		criticalDamage = self.datas[PropertyType.CriticalDamage].get()
		return criticalDamage
	
	def getAttackSpeed(self):
		'''获取攻击速度'''
		attackSpeed = self.datas[PropertyType.AttackSpeed].get()
		return attackSpeed

	def getMultiStrike(self):
		'''获取多重打击次数'''
		multiStrike = self.datas[PropertyType.MultiStrike].get()
		return multiStrike
	
	def getMagazineSize(self) -> int:
		'''获取弹容量'''
		magazineSize = self.datas[PropertyType.MagazineSize].get()
		magazineSize = int(round(magazineSize))
		return magazineSize
	
	def getReloadTime(self) -> float:
		'''获取装填时间'''
		reloadTime = self.datas[PropertyType.ReloadTime].get()
		return reloadTime
	
	# 造成一次伤害
	def MakeDamage(self) -> DamageCollection:
		return self.damageSnapshot

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
					find, property = FindElementDamage(PropertyType.Gas)
					if not find:
						find, property = FindElementDamage(PropertyType.Ether)
			elif propertyType == PropertyType.Cold:
				find, property = FindElementDamage(PropertyType.Cracking)
				if not find:
					find, property = FindElementDamage(PropertyType.Magnetic)
					if not find:
						find, property = FindElementDamage(PropertyType.Virus)
			elif propertyType == PropertyType.Electric:
				find, property = FindElementDamage(PropertyType.Radiation)
				if not find:
					find, property = FindElementDamage(PropertyType.Magnetic)
					if not find:
						find, property = FindElementDamage(PropertyType.Ether)
			elif propertyType == PropertyType.Poison:
				find, property = FindElementDamage(PropertyType.Virus)
				if not find:
					find, property = FindElementDamage(PropertyType.Gas)
					if not find:
						find, property = FindElementDamage(PropertyType.Radiation)
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
					# 如果有赛能，复合成磁暴
					property.value += elementDamageArray[i].get()
					property.addon = 0.0
					property.propertyType = PropertyType.Magnetic
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
							# 如果有热波，复合成裂化
							property.value += elementDamageArray[i].get()
							property.addon = 0.0
							property.propertyType = PropertyType.Cracking
							continue
			elif damageType == PropertyType.Electric:
				# 赛能
				find, property = FindElementDamage(PropertyType.Fire)
				if find:
					# 如果有热波，复合成以太
					property.value += elementDamageArray[i].get()
					property.addon = 0.0
					property.propertyType = PropertyType.Ether
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
							# 如果有创生，复合成辐射
							property.value += elementDamageArray[i].get()
							property.addon = 0.0
							property.propertyType = PropertyType.Radiation
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
							# 如果有冰冻，复合成病毒
							property.value += elementDamageArray[i].get()
							property.addon = 0.0
							property.propertyType = PropertyType.Virus
							continue
			# 如果没有可复合的元素伤害，直接添加到FinalDamageArray
			FinalDamageArray.append(copy.deepcopy(elementDamageArray[i]))
		
		# 别忘了将那些addon还有值的属性也都计算一次，比如……动能
		for propertyType in PropertyType:
			if propertyType.isDamage() and self.datas[propertyType].addon != 0:
				self.datas[propertyType].value = self.datas[propertyType].addon * baseDamage / 100.0
				self.datas[propertyType].addon = 0.0

		# 将FinalDamageArray中的元素伤害添加到快照中
		for property in FinalDamageArray:
			if property.propertyType.isElementDamage():
				self.datas[property.propertyType].add(property, ignore_type_check=True)
			else:
				raise ValueError("Invalid property type for element damage")

		# 最后将对所有伤害进行AllDamage的加成
		allDamageAddon = self.datas[PropertyType.AllDamage].addon / 100.0
		for propertyType in PropertyType:
			if propertyType.isDamage():
				self.datas[propertyType].value *= (1 + allDamageAddon)
				self.datas[propertyType].addon = 0.0			
			
		# 更新伤害快照
		self.damageSnapshot = DamageCollection.createDamage([
			self.datas[PropertyType.Physics].get(),
			self.datas[PropertyType.Cold].get(),
			self.datas[PropertyType.Electric].get(),
			self.datas[PropertyType.Fire].get(),
			self.datas[PropertyType.Poison].get(),
			self.datas[PropertyType.Cracking].get(),
			self.datas[PropertyType.Radiation].get(),
			self.datas[PropertyType.Gas].get(),
			self.datas[PropertyType.Magnetic].get(),
			self.datas[PropertyType.Ether].get(),
			self.datas[PropertyType.Virus].get()
		])

	def update_ghost(self, propertiesArray : list, ghostSetNum: int):
		'''
		魈鬼系列应用另一套伤害公式
		:param ghostSetNum: 武器里魈鬼系列套装数量
		'''
		# 魈鬼系列应用另一套伤害公式，不过先要计算出未转化为动能伤害之前的伤害
		self.update(propertiesArray)
		ghostNum = ghostSetNum + env.SetNum[CardSet.Ghost.value]
		totalDamage = self.getTotalDamage()
		physicsDamage = self.datas[PropertyType.Physics].get()
		convertedPhysicsDamage = (totalDamage - physicsDamage) * ghostNum + physicsDamage
		# 清空伤害属性
		for propertyType in PropertyType:
			if propertyType.isElementDamage():
				self.datas[propertyType].clear()
		self.datas[PropertyType.Physics].addon = 0.0
		self.datas[PropertyType.Physics].value = convertedPhysicsDamage
		# 更新伤害快照
		self.damageSnapshot = DamageCollection.createDamage([
			self.datas[PropertyType.Physics].get(),
			self.datas[PropertyType.Cold].get(),
			self.datas[PropertyType.Electric].get(),
			self.datas[PropertyType.Fire].get(),
			self.datas[PropertyType.Poison].get(),
			self.datas[PropertyType.Cracking].get(),
			self.datas[PropertyType.Radiation].get(),
			self.datas[PropertyType.Gas].get(),
			self.datas[PropertyType.Magnetic].get(),
			self.datas[PropertyType.Ether].get(),
			self.datas[PropertyType.Virus].get()
		])

# 所有卡牌的基类
class CardBase:
	def __init__(self, name, cost : int = 0, weaponType: WeaponType = None):
		self.name = name
		self.weaponType = weaponType
		self.cost = cost

	@abstractmethod
	def getProperties(self):
		pass

class CardCommon(CardBase):
	# 常规卡牌，只有一条属性
	def __init__(self, name, property: Property, cost : int = 0, weaponType: WeaponType = None, cardSet: CardSet = CardSet.Unset):
		super().__init__(name, cost, weaponType)
		self.property = property
		self.cardSet = cardSet

	def getProperties(self):
		return [copy.deepcopy(self.property)]

class CardRiven(CardBase):
	# 紫卡，可拥有多条属性
	def __init__(self, name, properties : list, cost : int = 0, WeaponType: WeaponType = None):
		super().__init__(name, cost, WeaponType)
		self.properties = properties

	def getProperties(self):
		'''返回卡牌的属性列表'''
		properties = []
		for property in self.properties:
				properties.append(copy.deepcopy(property))
		return properties

# 所有武器的基类
class WeaponBase:
	def __init__(self, name, baseProperties : PropertySnapshot, weaponType : WeaponType = WeaponType.Rifle, basename=None, isPrime=False):
		self.name = name
		self.baseProperties = baseProperties
		self.currentProperties = None
		self.cards = [None, None, None, None, None, None, None, None]  # 最多8张卡牌
		self._dirty = True  # 是否需要更新当前属性
		if basename is None:
			self.basename = name
		else:
			self.basename = basename
		self.isPrime = isPrime
		self.weaponType = weaponType

	# 安装卡牌
	def setCardAtIndex(self, index, card : CardBase):
		if index < 0 or index >= 8:
			raise IndexError("Index out of range")
		self.cards[index] = card
		self._dirty = True  # 设置为需要更新当前属性

	def setCardPermutes(self, cards : list):
		'''设置卡牌的排列组合'''
		if (len(cards) == 8):
			self.cards = cards
			self._dirty = True

	def removeCardAtIndex(self, index):
		if index < 0 or index >= 8:
			raise IndexError("Index out of range")
		self.cards[index] = None
		self._dirty = True
		
	def getCardAtIndex(self, index):
		if index < 0 or index >= 8:
			raise IndexError("Index out of range")
		return self.cards[index]
	
	def updateCurrentProperties(self):
		if not self._dirty:
			return
		self.currentProperties = copy.deepcopy(self.baseProperties)
		GhostSetNum = 0
		for card in self.cards:
			if isinstance(card, CardCommon) and card.cardSet == CardSet.Ghost:
				GhostSetNum += 1
		if GhostSetNum > 0:
			propertyArray = []
			for card in self.cards:
				if card is not None:
					propertyArray.extend(card.getProperties())
			self.currentProperties.update_ghost(propertyArray, GhostSetNum)
		else:
			propertyArray = []
			for card in self.cards:
				if card is not None:
					propertyArray.extend(card.getProperties())
			self.currentProperties.update(propertyArray)
		self._dirty = False

	def printAllProperties(self):
		if self.currentProperties is None:
			self.updateCurrentProperties()
		print(f"Weapon: {self.name}")
		print(f"Total Damage: {self.currentProperties.getTotalDamage()}")
		for propertyType, property in self.currentProperties.datas.items():
			if property.get() != 0:
				print(f"{propertyType.toString()}: {property.get()}")
		print("Cards:")
		for card in self.cards:
			if card is not None:
				print(f"- {card.name}")

	def getCardSetNum(self, cardSet: CardSet):
		'''获取指定套装卡牌的数量'''
		if cardSet == CardSet.Unset:
			return 0
		count = 0
		for card in self.cards:
			if isinstance(card, CardCommon) and card.cardSet == cardSet:
				count += 1
		return count

# 所有异常状态的基类
class DebuffBase:
	def __init__(self, duration):
		self.duration = duration
		self.time = 0

class DebuffQueue:
	def __init__(self, maxLayers=-1, constantCount=0):
		self.queue = []
		self.maxLayers = maxLayers
		self.constantCount = constantCount

	def addDebuff(self, debuff: DebuffBase):
		'''触发元素异常'''
		if self.maxLayers < 0:
			self.queue.append(debuff)
		else:
			# 如果当前层数小于最大层数，直接添加
			if len(self.queue) < self.maxLayers:
				self.queue.append(debuff)
			else:
				# 如果当前层数已经达到最大层数，替换掉最早的一个
				self.queue.pop(0)
				self.queue.append(debuff)

	def setConstantCount(self, count):
		'''设置不会消退的异常层数'''
		self.constantCount = count if self.maxLayers < 0 else min(count, self.maxLayers)

	def count(self) -> int:
		'''获取当前队列中的debuff数量'''
		return min(len(self.queue) + self.constantCount, self.maxLayers) if self.maxLayers >= 0 else len(self.queue) + self.constantCount

# 所有敌人的基类
class EnemyBase:
	def __init__(self, name, level, material):
		self.name = name
		self.level = level
		self.material = material
		self.debuff = [
			DebuffQueue(),	# 动能，但不需要
			DebuffQueue(9),  # 冰冻
			DebuffQueue(),  # 赛能
			DebuffQueue(),  # 热波
			DebuffQueue(),  # 创生
			DebuffQueue(),  # 裂化
			DebuffQueue(10),  # 辐射
			DebuffQueue(),  # 毒气
			DebuffQueue(10),  # 磁暴
			DebuffQueue(10),  # 以太
			DebuffQueue(10),  # 病毒
		]
		self.armor = 0.0
		self.health = 0.0
		self.shield = 0.0

	def setConstantDebuff(self, propertyType: PropertyType, count: int):
		'''设置不会消退的异常层数'''
		if propertyType.isElementDamage():
			self.debuff[propertyType.value].setConstantCount(count)
		else:
			raise ValueError("Invalid property type for constant debuff")
		
	def addDebuff(self, propertyType: PropertyType, debuff: DebuffBase):
		'''添加元素异常'''
		if propertyType.isElementDamage():
			self.debuff[propertyType.value].addDebuff(debuff)
		else:
			raise ValueError("Invalid property type for debuff")
		
	def clearDebuff(self):
		'''清除元素异常'''
		for debuffQueue in self.debuff:
			debuffQueue.queue.clear()

	def printEnemyInfo(self):
		print(f"当前敌人")
		print(f"材质: {self.material.toString()}")
		print(f"护甲: {self.armor}")
		for propertyType, debuffQueue in enumerate(self.debuff):
			if debuffQueue.count() > 0:
				print(f"{PropertyType(propertyType).toString()} 层数: {debuffQueue.count()}")