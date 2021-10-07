from enum import Enum

from stats import Stats


class ItemKind(Enum):
    WEAPON = 0
    TOOL = 1
    EQUIPMENT = 2
    OBJECT = 3


class Item:
    kind: ItemKind
    name: str = None

    def __init__(self, name: str = None):
        if not self.name:
            self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Item: {self.name} ({self.stats})'


class Weapon(Item):
    kind: ItemKind = ItemKind.WEAPON
    stats: Stats = Stats()


class Sword(Weapon):
    name: str = "Sword"
    stats = Stats(hab=4)


class Spear(Weapon):
    name = 'Spear'
    stats = Stats(hab=3, adr=1)


class Morgentern(Weapon):
    name = 'Morgenstern'
    stats = Stats(hab=1, end=1, deg=1)


class Bow(Weapon):
    name = 'Bow'
    stats = Stats(hab=3, adr=1, crit=4)


class Tool(Item):
    pass


class KitEscalade(Tool):
    name = 'Kit d\'escalade'
    stats = Stats(adr=1)


class Dagger(Tool):
    name = 'Dague'
    stats = Stats(hab=1, crit=6)


class Equipment(Item):
    pass


class Pamphlet(Equipment):
    name = 'Pamphlet'
    stats = Stats(cha=4)


class SacDeGrain(Item):
    name = 'Sac de grains'
    stats = Stats(end=2, cha=2)
