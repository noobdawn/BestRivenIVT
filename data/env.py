from core.ivtenum import *
from core.baseclass import *



# 身上有几个MOD套装
class CardSetInfo:
	SetNum = []

	def __init__(self):
		self.SetNum = []
		for _ in CardSet:
			self.SetNum.append(0)

	def hasCardSet(self, cardSet: CardSet) -> bool:
		return self.SetNum[cardSet.value] > 0
	
	def getCardSetNum(self, cardSet: CardSet) -> int:
		return self.SetNum[cardSet.value]
	
	def setCardSetNum(self, cardSet: CardSet, num: int):
		self.SetNum[cardSet.value] = num
	
# 角色动作状态
class MoveState:
	isMoving = False
	isInAir = False
	isAiming = False
	sniperComboMulti = 1.0

	def __init__(self):
		self.isMoving = False
		self.isInAir = False
		self.isAiming = False
		self.sniperComboMulti = 1.0

# 角色加成状态
class CharacterBuffState:
	def __init__(self):
		pass


# 角色
class Character:
	def __init__(self, armor : ArmorBase):
		self.moveState = MoveState()
		self.cardSetInfo = CardSetInfo()
		self.buffState = CharacterBuffState()
		self.armor = armor


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


# 靶子
class DebuffState:
	def __init__(self):
		self.elementDebuff = [
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
		# 因技能造成的Debuff
		self.skillDebuff = {
			SkillFlag.Qianyinfeidan : False,
			SkillFlag.Dianlizhenya : False,
		}

	def setConstantElementDebuff(self, propertyType: PropertyType, count: int):
		'''设置不会消退的异常层数'''
		if propertyType.isElementDamage():
			self.elementDebuff[propertyType.value].setConstantCount(count)
		else:
			raise ValueError("Invalid property type for constant debuff")
		
	def addElementDebuff(self, propertyType: PropertyType, debuff: DebuffBase):
		'''添加元素异常'''
		if propertyType.isElementDamage():
			self.elementDebuff[propertyType.value].addDebuff(debuff)
		else:
			raise ValueError("Invalid property type for debuff")
		
	def clearElementDebuff(self):
		'''清除元素异常'''
		for debuffQueue in self.elementDebuff:
			debuffQueue.queue.clear()

class Target(EnemyBase):
	def __init__(self):
		super().__init__("靶子", 120, EnemyMaterial.Mechanical)
		self.armor = 850
		self.debuffState = DebuffState()

	def getArmor(self) -> float:
		'''获取当前护甲值'''
		return self.armor

	def getElementDebuff(self, propertyType: PropertyType) -> int:
		'''获取当前异常层数'''
		if propertyType.isElementDamage():
			return self.debuffState.elementDebuff[propertyType.value].count()
		else:
			raise ValueError("Invalid property type for debuff")
		
	def getSkillDebuff(self, skillFlag: SkillFlag) -> bool:
		'''获取当前技能易伤状态'''
		if skillFlag in self.debuffState.skillDebuff:
			return self.debuffState.skillDebuff[skillFlag]
		else:
			raise ValueError("Invalid skill flag for debuff")
		
	def clearElementDebuff(self):
		'''清除元素异常'''
		self.debuffState.clearElementDebuff()

	def addElementDebuff(self, propertyType: PropertyType, debuff: DebuffBase):
		'''添加元素异常'''
		self.debuffState.addElementDebuff(propertyType, debuff)

class Context:
	def __init__(self, armor : ArmorBase, weapon : WeaponBase):
		self.character = Character(armor)
		self.target = Target()
		self.weapon = weapon

	# 设置套装MOD数量
	def SetCardSetNum(self, cardSet: CardSet, num: int):
		self.character.cardSetInfo.setCardSetNum(cardSet, num)

	# 设置技能强度
	def SetCharacterSkillStrength(self, strength: float):
		self.character.armor.setProperty(CharacterPropertyType.SkillStrength, strength)

	# 设置元素异常
	def SetTargetElementDebuff(self, propertyType: PropertyType, count: int):
		self.target.debuffState.setConstantElementDebuff(propertyType, count)

	# 设置技能易伤
	def SetTargetSkillDebuff(self, skillFlag: SkillFlag, isActive: bool):
		if skillFlag in self.target.debuffState.skillDebuff:
			self.target.debuffState.skillDebuff[skillFlag] = isActive
		else:
			raise ValueError("Invalid skill flag for debuff")
		
	# 获取卡牌套装数量
	def getCardSetNum(self, cardSet: CardSet) -> int:
		return self.character.cardSetInfo.getCardSetNum(cardSet)
	
	def hasCardSet(self, cardSet: CardSet) -> bool:
		return self.character.cardSetInfo.hasCardSet(cardSet)
	
	def IsMoving(self) -> bool:
		return self.character.moveState.isMoving
	
	def IsInAir(self) -> bool:
		return self.character.moveState.isInAir
	
	def IsAiming(self) -> bool:
		return self.character.moveState.isAiming
	
	def GetSniperComboMulti(self) -> float:
		return self.character.moveState.sniperComboMulti
		
	# 打印当前环境信息
	def printEnvironment(self):
		print("当前环境信息:")
		print("角色属性:")
		print("  装甲: " + self.character.armor.armorSet.toString())
		for propType in CharacterPropertyType:
			print(f"  {propType.toString()}: {self.character.armor.getProperty(propType)}")
		print("套装MOD数量:")
		for cardSet in CardSet:
			if self.character.cardSetInfo.hasCardSet(cardSet):
				print(f"  {cardSet.toString()}: {self.character.cardSetInfo.getCardSetNum(cardSet)}")
		print("靶子基本信息:")
		print(f"  名称: {self.target.name}")
		print(f"  材质: {self.target.material.toString()}")
		print(f"  装甲: {self.target.armor}")
		print("靶子异常状态:")
		for propType in PropertyType:
			if propType.isElementDamage():
				count = self.target.debuffState.elementDebuff[propType.value].count()
				if count > 0:
					print(f"  {propType.toString()} 异常层数: {count}")
		for skillFlag, isActive in self.target.debuffState.skillDebuff.items():
			if isActive:
				print(f"  技能易伤: {skillFlag.toString()}")