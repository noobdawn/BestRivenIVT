# 该文件记叙了所有配装器定义的枚举值和相关方法
from enum import Enum, unique

@unique
class CardSet(Enum):
	'''
	套卡类型
	不过部分非套卡也使用这个枚举进行管理，例如光环卡-侵犯光环
	'''
	Unset = 0		# 不是套装卡片
	Reverse = 1		# 逆转，每张卡加30%暴击
	Ghost = 2		# 鬼卡，元素转动能
	Invasion = 3	# 侵犯光环，增加30%伤害
	Snake = 4		# 蛇年活动卡

	def toString(self):
		if self in CardSetToString:
			return CardSetToString[self]
		else:
			raise ValueError(f"Unknown CardSet: {self}")

CardSetToString = {
	CardSet.Unset: "非套装卡片",
	CardSet.Reverse: "逆转系列",
	CardSet.Ghost: "魈鬼系列",
	CardSet.Invasion: "侵犯光环",
	CardSet.Snake: "蛇年活动卡"
}

@unique
class EnemyMaterial(Enum):
	Void = 0
	Mechanical = 1
	Biological = 2
	Energy = 3

	def toString(self):
		if self in EnemyMaterialToString:
			return EnemyMaterialToString[self]
		else:
			raise ValueError(f"Unknown EnemyMaterial: {self}")

EnemyMaterialToString = {
	EnemyMaterial.Void: "虚空",
	EnemyMaterial.Mechanical: "机械",
	EnemyMaterial.Biological: "生物",
	EnemyMaterial.Energy: "能量"
}


class PropertyType(Enum):
	# 伤害类型
	Physics = 0
	Cold = 1
	Electric = 2
	Fire = 3
	Poison = 4
	# 复合伤害类型
	Cracking = 5
	Radiation = 6
	Gas = 7
	Magnetic = 8
	Ether = 9
	Virus = 10
	# 暴击
	CriticalChance = 11
	CriticalDamage = 12
	# 触发
	TriggerChance = 13
	# 攻击速度
	AttackSpeed = 14
	# 多重
	MultiStrike = 15
	# 弱点伤害
	Headshot = 16
	# 异常持续时间
	DebuffDuration = 17
	# 弹容量
	MagazineSize = 18
	# 装填时间
	ReloadTime = 19
	# 穿甲率和穿甲值
	PenetrationRate = 20
	PenetrationValue = 21
	# 武器伤害
	AllDamage = 22
	# 最大枚举
	_Max = 23
	_Damage = 11
	
	def isBaseElementDamage(self):
		'''判断是否是基础元素伤害'''
		# 基础元素伤害是指冰冻、赛能、热波、创生
		return self.value > 0 and self.value <= 4
	
	def isElementDamage(self):
		'''判断是否是元素伤害'''
		# 元素伤害是指基础元素伤害和复合元素伤害
		return self.value > 0 and self.value <= 10
	
	def isDamage(self):
		'''判断是否是伤害类型'''
		# 伤害类型是指动能伤害和元素伤害
		return self.value <= 10
	
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

@unique
class WeaponType(Enum):
	All = 0
	Rifle = 1
	MachineGun = 2
	Laser = 3
	RocketLauncher = 4
	Melee = 5
	Pistol = 6
	SubmachineGun = 7
	Sniper = 8
	Shotgun = 9
