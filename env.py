from ivtenum import CardSet

# 提供DPS测试时候的其他环境变量
class Environment:
	isMoving = False
	isInAir = False
	isAiming = False
	SetNum = []              		# 套装卡牌数量
	considerExclusiveCards = False  # 是否考虑专属卡牌
	sniperComboMulti = 1.0          # 狙击枪连击倍率
	useNianSkill = False            # 是否使用年春秋技能
	nianSkillStrength = 100			# 年春秋技能强度

	def __init__(self):
		self.reset()

	def printEnvironment(self):
		print("当前环境:")
		print(f"{'移动中' if self.isMoving else '静止'} | "
			  f"{'空中' if self.isInAir else '地面'} | "
			  f"{'瞄准中' if self.isAiming else '非瞄准'}")
		for cardSet in CardSet:
			if self.SetNum[cardSet.value] > 0:
				print(f"{cardSet.toString()} 数量: {self.SetNum[cardSet.value]}")
		if self.useNianSkill:
			print(f"使用年春秋技能，强度: {self.nianSkillStrength}")

	def reset(self):
		self.isMoving = False
		self.isInAir = False
		self.isAiming = False
		self.SetNum = []
		for _ in CardSet:
			self.SetNum.append(0)
		self.considerExclusiveCards = False
		self.sniperComboMulti = 1.0
		self.useNianSkill = False
		self.nianSkillStrength = 100

env = Environment()