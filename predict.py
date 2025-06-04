from core import *
from cards import *

waterdrop_prime = WeaponBase("私法 水滴", PropertySnapshot([
    Property(PropertyType.Physics, 0.0),
    Property(PropertyType.Cold, 0.0),
    Property(PropertyType.Electric, 0.0),
    Property(PropertyType.Poison, 0.0),
    Property(PropertyType.Fire, 0.0),
    Property(PropertyType.Cracking, 0.0),
    Property(PropertyType.Radiation, 0.0),
    Property(PropertyType.Gas, 0.0),
    Property(PropertyType.Magnetic, 0.0),
    Property(PropertyType.Ether, 31.0),
    Property(PropertyType.Virus, 0.0),
    Property(PropertyType.CriticalChance, 26.0),
    Property(PropertyType.CriticalDamage, 170.0),
    Property(PropertyType.MultiStrike, 1.0),
    Property(PropertyType.TriggerChance, 17.0),
    Property(PropertyType.AttackSpeed, 8.5),
    Property(PropertyType.DebuffDuration, 100.0),
    Property(PropertyType.MagazineSize, 32),
    Property(PropertyType.ReloadTime, 1.7),
    Property(PropertyType.PenetrationRate, 80),
]))
waterdrop_prime.setCardAtIndex(1, getRifleCards("增压枪膛"))
waterdrop_prime.setCardAtIndex(0, getRifleCards("零度弹头"))
waterdrop_prime.setCardAtIndex(6, getRifleCards("弹孔注射"))
waterdrop_prime.updateCurrentProperties()
waterdrop_prime.printAllProperties()