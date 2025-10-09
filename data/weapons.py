from core.baseclass import *

class WaterDrop_Prime(WeaponBase):
    def __init__(self):
        super().__init__("私法 水滴", PropertySnapshot([
        Property(PropertyType.Ether, 31.0),
        Property(PropertyType.CriticalChance, 26.0),
        Property(PropertyType.CriticalDamage, 170.0),
        Property(PropertyType.MultiStrike, 1.0),
        Property(PropertyType.TriggerChance, 17.0),
        Property(PropertyType.AttackSpeed, 8.5),
        Property(PropertyType.DebuffDuration, 100.0),
        Property(PropertyType.MagazineSize, 32),
        Property(PropertyType.ReloadTime, 1.7),
        Property(PropertyType.PenetrationRate, 80),
    ]), WeaponType.Rifle, "水滴", True)
        
class Arcturus_Primer(WeaponBase):
    def __init__(self):
        super().__init__("私法 大角星", PropertySnapshot([
        Property(PropertyType.Physics, 25.0),
        Property(PropertyType.Cold, 35.0),
        Property(PropertyType.CriticalChance, 19.0),
        Property(PropertyType.CriticalDamage, 210.0),
        Property(PropertyType.MultiStrike, 1.0),
        Property(PropertyType.TriggerChance, 27.0),
        Property(PropertyType.AttackSpeed, 6),
        Property(PropertyType.DebuffDuration, 100.0),
        Property(PropertyType.MagazineSize, 20),
        Property(PropertyType.ReloadTime, 1.9),
    ]), WeaponType.Rifle, "大角星", True)
        
class FocusLamp(WeaponBase):
    def __init__(self):
        super().__init__("聚焦矿灯", PropertySnapshot([
        Property(PropertyType.Electric, 10.0),
        Property(PropertyType.Cracking, 9.0),
        Property(PropertyType.CriticalChance, 16.0),
        Property(PropertyType.CriticalDamage, 190.0),
        Property(PropertyType.MultiStrike, 1.0),
        Property(PropertyType.TriggerChance, 16.0),
        Property(PropertyType.AttackSpeed, 10.0),
        Property(PropertyType.DebuffDuration, 100.0),
        Property(PropertyType.MagazineSize, 35),
        Property(PropertyType.ReloadTime, 2),
    ]), WeaponType.Rifle, "聚焦矿灯", False)
        
class IceFall_Prime(WeaponBase):
    def __init__(self):
        super().__init__("私法 冰封瀑", PropertySnapshot([
        Property(PropertyType.Cold, 18.0),
        Property(PropertyType.CriticalChance, 24.0),
        Property(PropertyType.CriticalDamage, 170.0),
        Property(PropertyType.MultiStrike, 8.0),
        Property(PropertyType.TriggerChance, 7.0),
        Property(PropertyType.AttackSpeed, 3.5),
        Property(PropertyType.DebuffDuration, 100.0),
        Property(PropertyType.MagazineSize, 15),
        Property(PropertyType.ReloadTime, 2.2),
    ]), WeaponType.Shotgun, "冰封瀑", True)