# 提供DPS测试时候的其他环境变量
class Environment:
	isMoving = False
	isInAir = False
	isAiming = False
	SetNum = [0, 0, 0]              # 套装卡牌数量
	considerExclusiveCards = False  # 是否考虑专属卡牌
	invasionAuraNum = 0             # 侵犯光环数量
	sniperComboMulti = 1.0          # 狙击枪连击倍率
	useNianSkill = False            # 是否使用年春秋技能
	nianSkillStrength = 100			# 年春秋技能强度

	def printEnvironment(self):
		print(f"移动状态: {self.isMoving}\t空中状态: {self.isInAir}\t瞄准状态: {self.isAiming}")
		print(f"套装卡牌数量: {self.SetNum}")
		print(f"考虑专属卡牌: {self.considerExclusiveCards}")
		print(f"侵犯光环数量: {self.invasionAuraNum}")
		print(f"使用年春秋技能: {self.useNianSkill}")
		print(f"年春秋技能强度: {self.nianSkillStrength}")

	def reset(self):
		self.isMoving = False
		self.isInAir = False
		self.isAiming = False
		self.SetNum = [0, 0, 0]
		self.considerExclusiveCards = False
		self.invasionAuraNum = 0
		self.sniperComboMulti = 1.0
		self.useNianSkill = False
		self.nianSkillStrength = 100

env = Environment()