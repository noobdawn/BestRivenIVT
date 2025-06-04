from core import *
C = CardCommon
P = PropertyType
MOD = Property.createCardProperty

# 该文件记叙了所有的常规卡牌
RIFILE_CARDS = [
    C("私法 速效定装", MOD(P.ReloadTime, -60)),
    C("多重点射", MOD(P.MultiStrike, 90)),
    C("增压枪膛", MOD(P.AllDamage, 150)),
    C("逆转之心", MOD(P.CriticalChance, 100)),
    C("透镜校准", MOD(P.DebuffDuration, 100)),
    C("快速回膛", MOD(P.AttackSpeed, 50)),
    C("裸露铅心", MOD(P.CriticalDamage, 125)),
    C("长枪专家", MOD(P.TriggerChance, 75)),
    C("弹道修正", MOD(P.CriticalChance, 150)),
    C("扩容弹匣", MOD(P.MagazineSize, 30)),
    C("零度弹头", MOD(P.Cold, 75)),
    C("感生电圈", MOD(P.Electric, 75)),
    C("高温枪管", MOD(P.Fire, 75)),
    C("弹孔注射", MOD(P.Poison, 75)),
    C("致密打击", MOD(P.Physics, 50)),
]
for card in RIFILE_CARDS:
    card.weaponType = WeaponType.Rifle
