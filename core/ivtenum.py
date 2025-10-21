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
	Bless = 5		# 天佑，释放技能转换40%为护盾

	def __str__(self):
		if self in CardSetToString:
			return CardSetToString[self]
		else:
			raise ValueError(f"Unknown CardSet: {self}")

CardSetToString = {
	CardSet.Unset: "非套装卡片",
	CardSet.Reverse: "逆转系列",
	CardSet.Ghost: "魈鬼系列",
	CardSet.Invasion: "侵犯光环",
	CardSet.Snake: "蛇年活动卡",
	CardSet.Bless: "天佑系列"
}

AvailableCardSets = {
	CardSet.Reverse,
	CardSet.Ghost,
	CardSet.Invasion
}

@unique
class EnemyMaterial(Enum):
	Void = 0
	Mechanical = 1
	Biological = 2
	Energy = 3

	def __str__(self):
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
	# 空中暴击率
	CriticalChanceInAir = 100
	# 空中元素伤害
	ColdInAir = 101
	ElectricInAir = 102
	FireInAir = 103
	PoisonInAir = 104

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
	
	def __str__(self):
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
	PropertyType.AllDamage: "武器伤害",
	PropertyType.CriticalChanceInAir: "在空中时，暴击率",
	PropertyType.ColdInAir: "在空中时，冰冻伤害",
	PropertyType.ElectricInAir: "在空中时，赛能伤害",
	PropertyType.FireInAir: "在空中时，热波伤害",
	PropertyType.PoisonInAir: "在空中时，创生伤害"
}

@unique
class CharacterPropertyType(Enum):
	Health = 0
	Shield = 1
	Armor = 2
	Energy = 3
	DamageReduction = 4
	# 技能相关属性
	SkillStrength = 5
	SkillRange = 6
	SkillCost = 7
	SkillDuration = 8
	# 其他
	MoveSpeed = 9
	ShieldRechargeRate = 10
	ShieldRechargeDelay = 11

	def __str__(self):
		if self in CharacterPropertyTypeToString:
			return CharacterPropertyTypeToString[self]
		else:
			raise ValueError(f"Unknown CharacterPropertyType: {self}")
		
CharacterPropertyTypeToString = {
	CharacterPropertyType.Health: "生命值",
	CharacterPropertyType.Shield: "护盾值",
	CharacterPropertyType.Armor: "装甲值",
	CharacterPropertyType.Energy: "能量值",
	CharacterPropertyType.DamageReduction: "伤害减免",
	CharacterPropertyType.SkillStrength: "技能强度",
	CharacterPropertyType.SkillRange: "技能范围",
	CharacterPropertyType.SkillCost: "技能消耗",
	CharacterPropertyType.SkillDuration: "技能持续时间",
	CharacterPropertyType.MoveSpeed: "移动速度",
	CharacterPropertyType.ShieldRechargeRate: "护盾充能速率",
	CharacterPropertyType.ShieldRechargeDelay: "护盾充能延迟"
}

@unique
class WeaponType(Enum):
	All = 0
	Rifle = 1
	Shotgun = 2
	RocketLauncher = 3
	Melee = 4
	Pistol = 5

	def __str__(self):
		if self in WeaponTypeToString:
			return WeaponTypeToString[self]
		else:
			raise ValueError(f"Unknown WeaponType: {self}")
		
	def fromString(s: str):
		if s in StringToWeaponType:
			return StringToWeaponType[s]
		else:
			raise ValueError(f"Unknown WeaponType string: {s}")

WeaponTypeToString = {
	WeaponType.All: "所有武器",
	WeaponType.Rifle: "步枪",
	WeaponType.RocketLauncher: "发射器",
	WeaponType.Melee: "近战武器",
	WeaponType.Pistol: "手枪",
	WeaponType.Shotgun: "霰弹枪"
}

StringToWeaponType = {
	"All": WeaponType.All,
	"Rifle": WeaponType.Rifle,
	"Shotgun": WeaponType.Shotgun,
	"RocketLauncher": WeaponType.RocketLauncher,
	"Melee": WeaponType.Melee,
	"Pistol": WeaponType.Pistol
}

@unique
class SubWeaponType(Enum):
	Null = 0
	AssaultRifle = 1 # 突击步枪
	SniperRifle = 2 # 狙击枪
	MachineGun = 3 # 机枪
	LaserGun = 4 # 激光枪
	Shotgun = 5 # 霰弹枪
	RocketLauncher = 6 # 炮弹发射器
	Bow = 7 # 弓
	Kitana = 8 # 刀
	AutoPistol = 9 # 自动手枪
	MicroSubmachineGun = 10 # 微型冲锋枪

	def __str__(self):
		if self in SubWeaponTypeToString:
			return SubWeaponTypeToString[self]
		else:
			raise ValueError(f"Unknown SubWeaponType: {self}")
		
	def fromString(s: str):
		if s in StringToSubWeaponType:
			return StringToSubWeaponType[s]
		else:
			raise ValueError(f"Unknown SubWeaponType string: {s}")

SubWeaponTypeToString = {
	SubWeaponType.Null: "所有子类型",
	SubWeaponType.AssaultRifle: "突击步枪",
	SubWeaponType.SniperRifle: "狙击枪",
	SubWeaponType.MachineGun: "机枪",
	SubWeaponType.LaserGun: "激光枪",
	SubWeaponType.Shotgun: "霰弹枪",
	SubWeaponType.RocketLauncher: "炮弹发射器",
	SubWeaponType.Bow: "弓",
	SubWeaponType.Kitana: "刀",
	SubWeaponType.AutoPistol: "自动手枪",
	SubWeaponType.MicroSubmachineGun: "微型冲锋枪"
}

StringToSubWeaponType = {
	"All": SubWeaponType.Null,
	"AssaultRifle": SubWeaponType.AssaultRifle,
	"SniperRifle": SubWeaponType.SniperRifle,
	"MachineGun": SubWeaponType.MachineGun,
	"LaserGun": SubWeaponType.LaserGun,
	"Shotgun": SubWeaponType.Shotgun,
	"RocketLauncher": SubWeaponType.RocketLauncher,
	"Bow": SubWeaponType.Bow,
	"Kitana": SubWeaponType.Kitana,
	"AutoPistol": SubWeaponType.AutoPistol,
	"MicroSubmachineGun": SubWeaponType.MicroSubmachineGun
}

WeaponTypeToSubTypes = {
	WeaponType.Rifle: [SubWeaponType.AssaultRifle, SubWeaponType.SniperRifle, SubWeaponType.MachineGun, SubWeaponType.LaserGun],
	WeaponType.Shotgun: [SubWeaponType.Shotgun],
	WeaponType.RocketLauncher: [SubWeaponType.RocketLauncher, SubWeaponType.Bow],
	WeaponType.Melee: [SubWeaponType.Kitana],
	WeaponType.Pistol: [SubWeaponType.AutoPistol, SubWeaponType.MicroSubmachineGun]
}

@unique
# 角色枚举
class Hero(Enum):
	Nianchunqiu = 0 # 年春秋
	Taogongnuonuo = 1 # 桃宫诺诺
	Qiaoanna = 2 # 乔安娜·西奥斯
	Zhuli = 3 # 朱莉·摩恩
	Bickmen = 4 # 比克曼
	Pamera = 5 # 帕梅拉
	Shaokailin = 6 # 邵凯琳
	Mitera = 7 # 密特拉
	Lihuo = 8 # 离火
	Aier = 9 # 爱尔·斯宾塞
	Kirov = 10 # 基洛夫·瑞泊汀
	Shana = 11 # 莎娜

	def __str__(self):
		if self in HeroToString:
			return HeroToString[self]
		else:
			raise ValueError(f"Unknown Hero: {self}")

HeroToString = {
	Hero.Nianchunqiu: "年春秋",
	Hero.Taogongnuonuo: "桃宫诺诺",
	Hero.Qiaoanna: "乔安娜·西奥斯",
	Hero.Zhuli: "朱莉·摩恩",
	Hero.Bickmen: "比克曼",
	Hero.Pamera: "帕梅拉",
	Hero.Shaokailin: "邵凯琳",
	Hero.Mitera: "密特拉",
	Hero.Lihuo: "离火",
	Hero.Aier: "爱尔·斯宾塞",
	Hero.Kirov: "基洛夫·瑞泊汀",
	Hero.Shana: "莎娜"
}

@unique
# 装甲套装枚举
class ArmorSet(Enum):
	Shouzhanqibing = 0 # 首战奇兵
	Guangyin = 1 # 光阴
	Shouzhanqibing_Prime = 2 # 私法 首战奇兵
	Lvyechongming = 3 # 绿野虫鸣
	Lingtaifeixing = 4 # 灵态飞行
	Lingtaifeixing_Prime = 5 # 私法 灵态飞行
	Yinniaoguilin = 6 # 银鸟归林
	Guangyizhuangjia = 7 # 光翼装甲
	Qihuashengfang = 8 # 绮花盛放
	Bikemanxiansheng = 9 # 比克曼先生
	Pameiladeyixiaobu = 10 # 帕梅拉的一小步
	Dafuwengduoji = 11 # 大富翁多吉
	Jinpaizhiqinguan = 12 # 金牌执勤官
	Jinlinlieshou = 13 # 锦麟猎手
	Zhuanlunluohan = 14 # 转轮罗汉
	Guluan = 15 # 孤鸾
	Jianxishizhe = 16 # 间隙使者
	Zhenbaozhuanjia = 17 # 镇暴专家
	Kunshou = 18 # 困兽
	Kunshou_Prime = 19 # 私法 困兽

	def __str__(self):
		if self in ArmorSetToString:
			return ArmorSetToString[self]
		else:
			raise ValueError(f"Unknown ArmorSet: {self}")
		
	def isPrime(self) -> bool:
		'''判断是否是私法套装'''
		return self in [ArmorSet.Shouzhanqibing_Prime, ArmorSet.Lingtaifeixing_Prime, ArmorSet.Kunshou_Prime]

ArmorSetToString = {
	ArmorSet.Shouzhanqibing: "首战奇兵",
	ArmorSet.Guangyin: "光阴",
	ArmorSet.Shouzhanqibing_Prime: "私法 首战奇兵",
	ArmorSet.Lvyechongming: "绿野虫鸣",
	ArmorSet.Lingtaifeixing: "灵态飞行",
	ArmorSet.Lingtaifeixing_Prime: "私法 灵态飞行",
	ArmorSet.Yinniaoguilin: "银鸟归林",
	ArmorSet.Guangyizhuangjia: "光翼装甲",
	ArmorSet.Qihuashengfang: "绮花盛放",
	ArmorSet.Bikemanxiansheng: "比克曼先生",
	ArmorSet.Pameiladeyixiaobu: "帕梅拉的一小步",
	ArmorSet.Dafuwengduoji: "大富翁多吉",
	ArmorSet.Jinpaizhiqinguan: "金牌执勤官",
	ArmorSet.Jinlinlieshou: "锦麟猎手",
	ArmorSet.Zhuanlunluohan: "转轮罗汉",
	ArmorSet.Guluan: "孤鸾",
	ArmorSet.Jianxishizhe: "间隙使者",
	ArmorSet.Zhenbaozhuanjia: "镇暴专家",
	ArmorSet.Kunshou: "困兽",
	ArmorSet.Kunshou_Prime: "私法 困兽"
}

HeroToArmorSet = {
	Hero.Nianchunqiu: [ArmorSet.Shouzhanqibing, ArmorSet.Guangyin, ArmorSet.Shouzhanqibing_Prime],
	Hero.Taogongnuonuo: [ArmorSet.Lvyechongming, ArmorSet.Lingtaifeixing, ArmorSet.Lingtaifeixing_Prime],
	Hero.Qiaoanna: [ArmorSet.Yinniaoguilin],
	Hero.Zhuli: [ArmorSet.Guangyizhuangjia, ArmorSet.Qihuashengfang],
	Hero.Bickmen: [ArmorSet.Bikemanxiansheng],
	Hero.Pamera: [ArmorSet.Pameiladeyixiaobu, ArmorSet.Dafuwengduoji],
	Hero.Shaokailin: [ArmorSet.Jinpaizhiqinguan, ArmorSet.Jinlinlieshou],
	Hero.Mitera: [ArmorSet.Zhuanlunluohan],
	Hero.Lihuo: [ArmorSet.Guluan],
	Hero.Aier: [ArmorSet.Jianxishizhe],
	Hero.Kirov: [ArmorSet.Zhenbaozhuanjia],
	Hero.Shana: [ArmorSet.Kunshou, ArmorSet.Kunshou_Prime]
}

@unique
# 因为技能而获得的特殊标记
class SkillFlag(Enum):
	Qianyinfeidan = 0 # 牵引飞弹
	Dianlizhenya = 1 # 电离镇压

	def __str__(self):
		if self in SkillFlagToString:
			return SkillFlagToString[self]
		else:
			raise ValueError(f"Unknown SkillFlag: {self}")

SkillFlagToString = {
	SkillFlag.Qianyinfeidan: "牵引飞弹",
	SkillFlag.Dianlizhenya: "电离镇压"
}

@unique
# MOD的卡槽类型
class Slot(Enum):
	Jia = 0
	Yi = 1
	Bing = 2
	Ding = 3
	Wu = 4
	Ji = 5

SlotToString = {
	0 : "jia",
	1 : "yi",
	2 : "bing",
	3 : "ding",
	4 : "wu",
	5 : "ji",
}

SlotToText = {
	0 : "甲",
	1 : "乙",
	2 : "丙",
	3 : "丁",
	4 : "戊",
	5 : "己",
}

@unique
# 紫卡条目数量，确认有几个增益和几个减益
class RivenRange(Enum):
	PP = 0
	PPN = 1
	PPP = 2
	PPPN = 3

	def __str__(self):
		if self in RivenRangeToString:
			return RivenRangeToString[self]
		else:
			raise ValueError(f"Unknown RivenRange: {self}")

RivenRangeToString = {
	RivenRange.PP: "2 增益 0 减益",
	RivenRange.PPN: "2 增益 1 减益",
	RivenRange.PPP: "3 增益 0 减益",
	RivenRange.PPPN: "3 增益 1 减益",
}

# 记录了不同属性在紫卡上的取值范围
RivenRangeDict = {
	PropertyType.AllDamage : {
		WeaponType.Rifle : 165,
		WeaponType.Pistol : 165,
		WeaponType.RocketLauncher : 165,
		WeaponType.Shotgun : 165,
		WeaponType.Melee : 165
	},
	PropertyType.Headshot : {
		WeaponType.Rifle : 150,
		WeaponType.Pistol : 150,
		WeaponType.RocketLauncher : 150,
		WeaponType.Shotgun : 150,
		WeaponType.Melee : 150
	},
	PropertyType.AttackSpeed : {
		WeaponType.Rifle : 60,
		WeaponType.Pistol : 60,
		WeaponType.RocketLauncher : 60,
		WeaponType.Shotgun : 60,
		WeaponType.Melee : 0
	},
	PropertyType.CriticalChance : {
		WeaponType.Rifle : 150,
		WeaponType.Pistol : 150,
		WeaponType.RocketLauncher : 150,
		WeaponType.Shotgun : 150,
		WeaponType.Melee : 180
	},
	PropertyType.CriticalDamage : {
		WeaponType.Rifle : 120,
		WeaponType.Pistol : 120,
		WeaponType.RocketLauncher : 120,
		WeaponType.Shotgun : 120,
		WeaponType.Melee : 90
	},
	PropertyType.Physics : {
		WeaponType.Rifle : 120,
		WeaponType.Pistol : 120,
		WeaponType.RocketLauncher : 120,
		WeaponType.Shotgun : 120,
		WeaponType.Melee : 120
	},
	PropertyType.Cold : {
		WeaponType.Rifle : 90,
		WeaponType.Pistol : 90,
		WeaponType.RocketLauncher : 90,
		WeaponType.Shotgun : 90,
		WeaponType.Melee : 90
	},
	PropertyType.Electric : {
		WeaponType.Rifle : 90,
		WeaponType.Pistol : 90,
		WeaponType.RocketLauncher : 90,
		WeaponType.Shotgun : 90,
		WeaponType.Melee : 90
	},
	PropertyType.Fire : {
		WeaponType.Rifle : 90,
		WeaponType.Pistol : 90,
		WeaponType.RocketLauncher : 90,
		WeaponType.Shotgun : 90,
		WeaponType.Melee : 90
	},
	PropertyType.Poison : {
		WeaponType.Rifle : 90,
		WeaponType.Pistol : 90,
		WeaponType.RocketLauncher : 90,
		WeaponType.Shotgun : 90,
		WeaponType.Melee : 90
	},
	PropertyType.MagazineSize : {
		WeaponType.Rifle : 50,
		WeaponType.Pistol : 50,
		WeaponType.RocketLauncher : 50,
		WeaponType.Shotgun : 50,
		WeaponType.Melee : 0
	},
	PropertyType.ReloadTime : {
		WeaponType.Rifle : -50,
		WeaponType.Pistol : -50,
		WeaponType.RocketLauncher : -50,
		WeaponType.Shotgun : -50,
		WeaponType.Melee : 0
	},
	PropertyType.TriggerChance : {
		WeaponType.Rifle : 90,
		WeaponType.Pistol : 90,
		WeaponType.RocketLauncher : 90,
		WeaponType.Shotgun : 90,
		WeaponType.Melee : 90
	},
	PropertyType.MultiStrike : {
		WeaponType.Rifle : 90,
		WeaponType.Pistol : 90,
		WeaponType.RocketLauncher : 90,
		WeaponType.Shotgun : 90,
		WeaponType.Melee : 0
	}
}

# 记录了因为紫卡条目数量而造成的浮动数值
RivenRangeParams = {
	RivenRange.PP: 0.9925,
	RivenRange.PPN: 1.24,
	RivenRange.PPP: 0.75,
	RivenRange.PPPN: 0.94,
}

def calculate_riven_property_range(prop_type: PropertyType, weapon_type: WeaponType, riven_range: RivenRange):
	"""
	Calculates the min and max value for a given riven property.
	Returns a tuple (min_val, max_val).
	"""
	if prop_type not in RivenRangeDict or weapon_type not in RivenRangeDict[prop_type]:
		return None, None

	base_value = RivenRangeDict[prop_type][weapon_type]
	if base_value == 0:
		return 0, 0

	base_value *= RivenRangeParams[riven_range]

	if base_value < 0:
		return base_value, 0
	else:
		return 0, base_value
	
AvailableRivenProperties = [
	PropertyType.AllDamage,
	PropertyType.Headshot,
	PropertyType.AttackSpeed,
	PropertyType.CriticalChance,
	PropertyType.CriticalDamage,
	PropertyType.Physics,
	PropertyType.Cold,
	PropertyType.Electric,
	PropertyType.Fire,
	PropertyType.Poison,
	PropertyType.MagazineSize,
	PropertyType.ReloadTime,
	PropertyType.TriggerChance,
	PropertyType.MultiStrike
]