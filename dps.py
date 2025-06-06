# 该文件提供了dps的计算场合
from env import Environment
from core import *

np_Adjustment = np.array([
	[1,		1,		1,		1], 	# Physics
	[1.25,	0.85,	1,		1], 	# Cold
	[1,		1,		0.75,	1.25], 	# Electric
	[0.85,	1.25,	1,		1], 	# Fire
	[1,		1,		1.25,	0.75],  # Poison
	[1.5,	0.5,	1,		1.5],  # Cracking
	[0.5,	1.5,	1,		1.75],  # Radiation
	[1,		1,		1.75, 0.5],  # Gas
	[1,     1.75,  0.5,   1.75],  # Magnetic
	[1.75,  1,     0.5,   1],    # Ether
	[0.5,   1,     1.5,   1]     # Virus
])
def DamageTakenByMaterial(damage : DamageCollection, enemyMaterial: EnemyMaterial):
	'''
	计算敌人受到的伤害
	:param damage: 伤害集合
	:param enemyMaterial: 敌人材质
	:return: 计算后的伤害集合
	'''
	return DamageCollection.createDamage(np.multiply(damage.np_damage, np_Adjustment[:, enemyMaterial.value]))

# 护甲减伤计算公式
def ArmorDamageReduction(armor: float) -> float:
    """
    计算护甲减伤
    :param armor: 护甲值
    :return: 减伤比例
    """
    return 1 - (armor / (800 + armor))

# 使用辐射和热波伤害削弱护甲，同时算上首战奇兵剥皮
def WeakArmor(armor: float, radiationCount: int = 0, fireCount: int = 0, useNianSkill = False, NianSkillStrength: float = 100) -> float:
    """
    使用辐射和热波伤害削弱护甲
    :param armor: 护甲值
    :param radiationCount: 辐射伤害数量
    :param fireCount: 热波伤害数量
    :param useNianSkill: 是否使用年春秋技能
    :param NianSkillStrength: 年春秋技能强度
    :return: 削弱后的护甲值
    """
    skillWeak = 0
    if useNianSkill:
        skillWeak = NianSkillStrength / 100.0 * 0.6     # 年春秋技能削弱护甲60%, 取决于技能强度
        skillWeak *= 100
        skillWeak = round(skillWeak) / 100.0
    fireWeak = 0.5 if fireCount > 0 else 0              # 热波伤害削弱护甲50%
    radiationWeak = 0
    if radiationCount > 0:
        radiationWeak = 0.16 + (radiationCount - 1) * 0.06    # 辐射伤害削弱护甲16%，每层叠加辐射伤害额外增加6%
        radiationWeak = min(radiationWeak, 0.7)         # 最大削弱比例为70%
    return max(armor * (1 - skillWeak) * (1 - fireWeak) * (1 - radiationWeak), 0)

def GetCriticalMultiplier(weapon: WeaponBase, enemy: EnemyBase) -> tuple:
    '''
    计算暴击倍率
    :param weapon: 武器对象
    :param enemy: 敌人对象
    :return: (暴击倍率, 是否暴击)
    '''
    criticalChance = weapon.currentProperties.getCriticalChance()
    criticalDamage = weapon.currentProperties.getCriticalDamage()
    coldCount = enemy.debuff[PropertyType.Cold.value].count()
    coldCriticalDamage = 0
    if coldCount > 0:
        coldCriticalDamage = 0.1 + (coldCount - 1) * 0.05  # 冰冻debuff增加敌人受到的暴击伤害10%，每层叠加冰冻敌人受到的暴击伤害额外增加5%
    # 如果暴击几率为0，则直接返回1.0
    if criticalChance <= 0:
        return 1.0, 0
    elif criticalChance <= 100:
        if rand() < criticalChance / 100.0:  # 如果随机数小于暴击几率，则触发暴击
            return criticalDamage / 100.0 + coldCriticalDamage, 1
        else:
            return 1.0, 0
    else:
        lowerCriticalLevel = int(criticalChance / 100)
        upperCriticalLevel = lowerCriticalLevel + 1
        criticalLevel = lowerCriticalLevel
        if rand() < (criticalChance - lowerCriticalLevel * 100) / 100.0:  # 如果随机数小于暴击几率的余数部分，则触发更高等级的暴击
            criticalLevel = upperCriticalLevel
        return criticalLevel * (criticalDamage / 100.0 + coldCriticalDamage), criticalLevel

# 武器攻击一次，但不等于只造成一次伤害，因为有可能有多重射击，返回所有伤害
# 此处计入了：
# - 武器伤害
# - 外部伤害加成倍率
# - 暴击
def PullTriggerOnce(weapon: WeaponBase, enemy : EnemyBase, env: Environment) -> tuple:
    """
    模拟武器触发一次攻击，返回造成的伤害和伤害次数
    """
    multistrike = weapon.currentProperties.getMultiStrike()
    damage = copy.deepcopy(weapon.currentProperties.MakeDamage())   # 深拷贝当前属性的伤害，避免修改快照变化
    # todo: 这里还要考虑到像是光环或者逆转卡之类的伤害加成
    invasionAuraNum = env.SetNum[CardSet.Invasion.value]
    reverseSetNum = env.SetNum[CardSet.Reverse.value] + weapon.getCardSetNum(CardSet.Reverse)  # 逆转套装数量
    if not env.isMoving:
        reverseSetNum = 0   # 逆转套装仅在移动时生效
    damage *= 1 + invasionAuraNum * 0.3 + reverseSetNum * 0.3 + (env.sniperComboMulti - 1)  # 光环、逆转和狙击枪连击的伤害加成
    # 计算暴击对伤害的放大
    criticalMultiplier, criticalLevel = GetCriticalMultiplier(weapon, enemy)
    damage *= criticalMultiplier
    # 考虑到多重，可能需要多次制造伤害
    damageTimes = int(multistrike)  # 多重射击的整数部分
    if multistrike - int(multistrike) > 0:
        if rand() < (multistrike - int(multistrike)):
            damageTimes += 1
    return damage, damageTimes, criticalLevel

def VulnerableVirusMultiplier(enemy: EnemyBase) -> float:
    """
    计算易伤病毒倍率
    :param enemy: 敌人对象
    :return: 易伤病毒倍率
    """
    virusCount = enemy.debuff[PropertyType.Virus.value].count()
    if virusCount > 0:
        return 1.75 + 0.25 * virusCount  # 易伤病毒倍率为2，每层叠加病毒额外增加0.25
    return 1.0

# 实际对目标造成的伤害
# 此处计入了：
# - 伤害克制关系
# - 护甲减伤
# - 易伤倍率，todo：目前只考虑了病毒
def DamageTaken(damage: DamageCollection, enemy : EnemyBase) -> float:
    damageTaken = DamageTakenByMaterial(damage, enemy.material).sum()
    # 考虑削甲之后的护甲
    baseArmor = enemy.armor
    fireCount = enemy.debuff[PropertyType.Fire.value].count()
    radiationCount = enemy.debuff[PropertyType.Radiation.value].count()
    useNianSkill = env.useNianSkill
    NianSkillStrength = env.nianSkillStrength
    realArmor = WeakArmor(baseArmor, radiationCount, fireCount, useNianSkill, NianSkillStrength)
    damageTaken = damageTaken * ArmorDamageReduction(realArmor)
    # 考虑易伤倍率
    damageTaken *= VulnerableVirusMultiplier(enemy)
    # 未考虑技能增伤
    return damageTaken    

def CalculateDPSInMagazine(weapon: WeaponBase, enemy: EnemyBase, env: Environment) -> float:
    """
    计算一个弹匣的DPS
    :param weapon: 武器对象
    :param enemy: 敌人对象
    :param env: 环境变量
    :return: 弹匣DPS
    """
    magazine = weapon.currentProperties.getMagazineSize()
    damageTaken = 0
    for i in range(magazine):
        damage, damageTimes, criticalLevel = PullTriggerOnce(weapon, enemy, env)
        for j in range(damageTimes):
            # 计算每次造成的伤害
            damageTaken += DamageTaken(damage, enemy) * damageTimes
    attackSpeed = weapon.currentProperties.getAttackSpeed()
    return damageTaken / (magazine / attackSpeed)  # 弹匣伤害除以弹匣射速得到DPS

def CalculateAverageDPS(weapon: WeaponBase, enemy: EnemyBase, env: Environment) -> float:
    """
    计算平均DPS
    :param weapon: 武器对象
    :param enemy: 敌人对象
    :param env: 环境变量
    :return: 平均DPS
    """
    magazine = weapon.currentProperties.getMagazineSize()
    reloadTime = weapon.currentProperties.getReloadTime()
    totalDamage = 0
    for i in range(magazine):
        damage, damageTimes, criticalLevel = PullTriggerOnce(weapon, enemy, env)
        totalDamage += DamageTaken(damage, enemy) * damageTimes
    attackSpeed = weapon.currentProperties.getAttackSpeed()
    return totalDamage / (magazine / attackSpeed + reloadTime)