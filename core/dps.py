# 该文件提供了dps的计算场合
from data.env import Context
from core.baseclass import *

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

def GetCriticalMultiplier(ctx : Context) -> tuple:
    '''
    计算暴击倍率
    :param ctx : 当前环境上下文
    :return: (未暴击伤害倍率，暴击伤害倍率）
    '''
    weapon = ctx.weapon
    enemy = ctx.target
    criticalChance = weapon.currentProperties.getCriticalChance()
    criticalDamage = weapon.currentProperties.getCriticalDamage()
    coldCount = 0
    if enemy is not None:
        coldCount = enemy.getElementDebuff(PropertyType.Cold)
    coldCriticalDamage = 0
    if coldCount > 0:
        coldCriticalDamage = 0.1 + (coldCount - 1) * 0.05  # 冰冻debuff增加敌人受到的暴击伤害10%，每层叠加冰冻敌人受到的暴击伤害额外增加5%
    # 如果暴击几率为0，则直接返回1.0
    if criticalChance <= 0:
        return 1, 1
    elif criticalChance <= 100:
        return 1.0, criticalDamage / 100.0 + coldCriticalDamage
    else:
        lowerCriticalLevel = int(criticalChance / 100)
        upperCriticalLevel = lowerCriticalLevel + 1
        return lowerCriticalLevel * (criticalDamage / 100.0 + coldCriticalDamage), upperCriticalLevel * (criticalDamage / 100.0 + coldCriticalDamage)

def GetBaseWeaponDamage(weapon: WeaponBase) -> DamageCollection:
    """
    获取武器的基础伤害
    :param weapon: 武器对象
    :return: 基础伤害集合
    """
    # 获取武器当前属性的伤害快照
    return copy.deepcopy(weapon.currentProperties.MakeDamage())

def GetExternalDamageMultiplier(ctx : Context) -> float:
    '''
    获取外部伤害加成倍率
    :param ctx: 当前环境上下文
    :return: 外部伤害加成倍率
    '''
    weapon = ctx.weapon
    enemy = ctx.target
    invasionAuraNum = ctx.getCardSetNum(CardSet.Invasion)
    reverseSetNum = weapon.getCardSetNum(CardSet.Reverse) + ctx.getCardSetNum(CardSet.Reverse)
    if not ctx.IsMoving():
        reverseSetNum = 0   # 逆转套装仅在移动时生效
    return 1 + invasionAuraNum * 0.3 + reverseSetNum * 0.3 + (ctx.GetSniperComboMulti() - 1)  # 光环、逆转和狙击枪连击的伤害加成

# # 获得武器伤害
# # 此处计入了：
# # - 武器伤害
# # - 外部伤害加成倍率
# # - 暴击
# def GetWeaponDamage(weapon: WeaponBase, enemy : EnemyBase, env: Environment) -> tuple:
#     """
#     获取武器伤害
#     :param weapon: 武器对象
#     :param enemy: 敌人对象
#     :param env: 环境变量
#     :return: (未暴击伤害，暴击伤害）
#     """
#     damage = GetBaseWeaponDamage(weapon)   # 深拷贝当前属性的伤害，避免修改快照变化
#     # 计算外部伤害加成倍率
#     invasionAuraNum = env.SetNum[CardSet.Invasion.value]
#     reverseSetNum = env.SetNum[CardSet.Reverse.value] + weapon.getCardSetNum(CardSet.Reverse)
#     if not env.isMoving:
#         reverseSetNum = 0   # 逆转套装仅在移动时生效
#     damage *= 1 + invasionAuraNum * 0.3 + reverseSetNum * 0.3 + (env.sniperComboMulti - 1)  # 光环、逆转和狙击枪连击的伤害加成
#     # 计算暴击对伤害的放大
#     uncriticalMultiplier, criticalMultiplier = GetCriticalMultiplier(weapon, enemy)
#     return damage * uncriticalMultiplier, damage * criticalMultiplier

def VulnerableVirusMultiplier(ctx : Context) -> float:
    """
    计算易伤病毒倍率
    :param ctx: 当前环境上下文
    :return: 易伤病毒倍率
    """
    enemy = ctx.target
    virusCount = enemy.getElementDebuff(PropertyType.Virus)
    if virusCount > 0:
        return 1.75 + 0.25 * virusCount  # 易伤病毒倍率为2，每层叠加病毒额外增加0.25
    return 1.0

def DamageTakenDoT(damage : float, propertyType: PropertyType, ctx : Context) -> float:
    """
    计算持续伤害对敌人造成的实际伤害
    :param damage: 基础伤害
    :param propertyType: 伤害类型
    :param ctx: 当前环境上下文
    :return: 实际伤害
    """
    damageTaken = damage
    # 考虑削甲之后的护甲
    if propertyType != PropertyType.Cracking:
        baseArmor = ctx.target.getArmor()
        fireCount = ctx.target.getElementDebuff(PropertyType.Fire)
        radiationCount = ctx.target.getElementDebuff(PropertyType.Radiation)
        useNianSkill = ctx.target.getSkillDebuff(SkillFlag.Qianyinfeidan)
        NianSkillStrength = ctx.character.armor.getProperty(CharacterPropertyType.SkillStrength)
        realArmor = WeakArmor(baseArmor, radiationCount, fireCount, useNianSkill, NianSkillStrength)
        damageTaken = damage * ArmorDamageReduction(realArmor)
    # 考虑易伤倍率
    damageTaken *= VulnerableVirusMultiplier(ctx)
    # 未考虑技能增伤
    return damageTaken

# 实际对目标造成的伤害
# 此处计入了：
# - 伤害克制关系
# - 护甲减伤
# - 易伤倍率，todo：目前只考虑了病毒
def DamageTaken(damage: DamageCollection, ctx : Context) -> float:
     # 如果没有敌人，则直接返回伤害总和作为参考
    enemy = ctx.target
    damageTaken = DamageTakenByMaterial(damage, enemy.material).sum()
    # 考虑削甲之后的护甲
    baseArmor = enemy.armor
    fireCount = enemy.getElementDebuff(PropertyType.Fire)
    radiationCount = enemy.getElementDebuff(PropertyType.Radiation)
    useNianSkill = enemy.getSkillDebuff(SkillFlag.Qianyinfeidan)
    NianSkillStrength = ctx.character.armor.getProperty(CharacterPropertyType.SkillStrength)
    realArmor = WeakArmor(baseArmor, radiationCount, fireCount, useNianSkill, NianSkillStrength)
    damageTaken = damageTaken * ArmorDamageReduction(realArmor)
    # 考虑易伤倍率
    damageTaken *= VulnerableVirusMultiplier(ctx)
    # 未考虑技能增伤
    return damageTaken

def TriggerElementDebuff(damage : DamageCollection) -> PropertyType:
    '''
    根据元素在伤害中的占比触发元素异常
    '''
    r = rand()
    tmpDamage = copy.deepcopy(damage)
    tmpDamage.np_damage[PropertyType.Physics.value] = 0.0  # 动能伤害不触发元素异常
    totalElementDamage = tmpDamage.np_damage.sum()  # 计算元素伤害总和
    currentThreshold = 0.0
    for i in range(PropertyType.Cold.value, PropertyType.Virus.value + 1):
        currentThreshold += damage.np_damage[i] / totalElementDamage
        if r < currentThreshold:
            return PropertyType(i)
        
def CalculateDamageOnce(ctx : Context, baseWeaponDamage: DamageCollection = None, forceCritical : int = 0, forceTrigger : int = 0) -> float:
    '''
    计算单次造成的伤害
    '''
    weapon = ctx.weapon
    enemy = ctx.target
    if baseWeaponDamage is None:
        baseWeaponDamage = GetBaseWeaponDamage(weapon)
    externalDamageMultiplier = GetExternalDamageMultiplier(ctx)
    uncriticalMultiplier, criticalMultiplier = GetCriticalMultiplier(ctx)
    uncriticalDamage = baseWeaponDamage * uncriticalMultiplier * externalDamageMultiplier
    criticalDamage = baseWeaponDamage * criticalMultiplier * externalDamageMultiplier
    uncriticalDamageTaken = DamageTaken(uncriticalDamage, ctx)
    criticalDamageTaken = DamageTaken(criticalDamage, ctx)
    # 计算是否暴击，以得到直接伤害
    directDamageTaken = uncriticalDamageTaken
    criticalChance = weapon.currentProperties.getCriticalChance() / 100.0
    if forceCritical == 1 or (forceCritical == 0 and rand() < criticalChance):
        directDamageTaken = criticalDamageTaken
    # 持续伤害
    doTDamageTaken = 0.0
    # 计算是否触发元素异常
    if enemy is not None:
        # 计算元素异常触发几率
        triggerChance = weapon.currentProperties.getTriggerChance()
        if forceTrigger == 1 or (forceTrigger == 0 and rand() < triggerChance / 100.0):
            # 触发元素异常
            debuffProperty = TriggerElementDebuff(uncriticalDamage)
            if debuffProperty is not None:
                # 直接添加到敌人身上
                enemy.addElementDebuff(debuffProperty, DebuffBase(6))  # 添加元素异常
                # 如果是伤害类的Debuff，则其持续伤害总量计入到damageTaken中
                DoTMultiplier = 0.0
                if debuffProperty == PropertyType.Fire or debuffProperty == PropertyType.Electric or debuffProperty == PropertyType.Gas:
                    # 热波、赛能、毒气元素异常的持续伤害倍率为 0.5，持续6秒
                    DoTMultiplier = 0.5
                elif debuffProperty == PropertyType.Cracking:
                    # 裂化的伤害倍率为 0.35，持续6秒
                    DoTMultiplier = 0.35
                if DoTMultiplier > 0:
                    DoTDamage = baseWeaponDamage.sum() * externalDamageMultiplier * DoTMultiplier
                    doTDamageTaken = DamageTakenDoT(DoTDamage, debuffProperty, ctx) * 6

    return directDamageTaken + doTDamageTaken  # 返回直接伤害和持续伤害的总和


def CalculateMagazineDamage(ctx : Context) -> float:
    """
    计算一个弹匣造成的总伤害
    :param ctx: 当前环境上下文
    :return: 总伤害
    """
    weapon = ctx.weapon
    enemy = ctx.target
    magazine = weapon.currentProperties.getMagazineSize()
    baseWeaponDamage = GetBaseWeaponDamage(weapon)
    damageTaken = 0
    for i in range(magazine):
        # 计算多重打击次数
        multistrike = weapon.currentProperties.getMultiStrike()
        damageTimes = int(multistrike)
        if rand() < (multistrike - int(multistrike)):
            damageTimes += 1
        # 这里是实际造成伤害的地方
        for j in range(damageTimes):
            damageTaken += CalculateDamageOnce(ctx, baseWeaponDamage, forceCritical=0, forceTrigger=0)
    attackSpeed = weapon.currentProperties.getAttackSpeed()
    return damageTaken

def CalculateMagazineDPS(ctx : Context) -> float:
    """
    计算一个弹匣的DPS
    :param ctx: 当前环境上下文
    :return: 弹匣DPS
    """
    weapon = ctx.weapon
    magazine = weapon.currentProperties.getMagazineSize()
    magazineDamage = CalculateMagazineDamage(ctx)
    attackSpeed = weapon.currentProperties.getAttackSpeed()
    return magazineDamage / (magazine / attackSpeed)

def CalculateAverageDPS(ctx : Context) -> float:
    """
    计算平均DPS
    :param ctx: 当前环境上下文
    :return: 平均DPS
    """
    weapon = ctx.weapon
    magazine = weapon.currentProperties.getMagazineSize()
    reloadTime = weapon.currentProperties.getReloadTime()
    magazineDamage = CalculateMagazineDamage(ctx)
    attackSpeed = weapon.currentProperties.getAttackSpeed()
    return magazineDamage / (magazine / attackSpeed + reloadTime)  # 弹匣伤害除以弹匣射速和换弹时间得到DPS