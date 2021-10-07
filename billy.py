from typing import List, Tuple
from enum import Enum
from functools import reduce
import operator
from random import randint
from contextlib import redirect_stdout

from stats import Stats
from items import Item, ItemKind, Weapon, Tool, Equipment
from enemy import Enemy
from entity import Entity


SITUATION_TABLE = {
    -7: [(0, 12), (0, 9), (1, 8), (2, 6), (2, 5), (3, 4)],
    -6: [(1, 8), (1, 7), (1, 6), (2, 5), (2, 5), (3, 4)],
    -5: [(1, 7), (1, 6), (1, 5), (2, 5), (3, 4), (4, 4)],
    -4: [(1, 6), (2, 6), (2, 5), (2, 4), (3, 4), (4, 3)],
    -3: [(2, 2), (2, 5), (2, 4), (3, 4), (3, 3), (4, 3)],
    -2: [(2, 6), (2, 5), (2, 4), (3, 3), (4, 3), (5, 3)],
    -1: [(3, 6), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3)],
    0: [(3, 5), (3, 4), (3, 3), (3, 3), (4, 3), (5, 3)],
    1: [(3, 5), (3, 5), (3, 3), (4, 3), (5, 3), (6, 3)],
    2: [(3, 5), (3, 4), (3, 3), (4, 2), (5, 2), (6, 2)],
    3: [(3, 4), (3, 3), (4, 3), (4, 2), (5, 2), (6, 2)],
    4: [(3, 4), (3, 4), (4, 2), (5, 2), (6, 2), (6, 1)],
    5: [(4, 4), (4, 3), (5, 2), (5, 1), (6, 1), (7, 1)],
    6: [(4, 3), (5, 2), (5, 2), (6, 1), (7, 1), (8, 1)],
    7: [(4, 3), (5, 2), (6, 2), (8, 1), (9, 0), (12, 0)]
}


class DeathException(Exception):
    pass


class BillyKind(Enum):
    WARRIOR = 'Guerrier'
    PEASANT = 'Paysant'
    CAREFULL = 'Prudent'
    DEBROUILLARD = 'Derbrouillard'


class Billy(Entity):
    name = 'Billy'
    luck_max: int
    kind: BillyKind
    base_stats = Stats(hab=2, end=2, adr=1, cha=3)
    items: List[Item] = []
    objects: List[Item] = []
    glory: int = 0
    richesse: int = 0
    path = []

    def __init__(self, items: List[Item]) -> None:
        assert len(items) == 3, 'You must have 3 items, no more, no less'
        self.items = items
        self.stats = self.get_stats()
        self.kind = self.get_kind()
        self._apply_class_perks()
        self.hp = self.stats.end * 3
        self.hp_max = self.hp
        self.luck_max = self.stats.cha

    def __repr__(self) -> str:
        return f'Billy ({self.stats}) [{self.hp}hp]'

    def mod_stats(self, modifier: Stats) -> None:
        self.stats += modifier

    def _apply_class_perks(self) -> None:
        kinds = {
            BillyKind.WARRIOR: Stats(hab=2, cha=-1),
            BillyKind.CAREFULL: Stats(cha=2, hab=-1),
            BillyKind.PEASANT: Stats(end=2, adr=-1),
            BillyKind.DEBROUILLARD: Stats(adr=2, end=-1)
        }
        self.stats += kinds[self.kind]

    def goto(self, chapter: int) -> None:
        self.path.append(chapter)

    @property
    def history(self):
        return self.path

    def get_items_stats(self) -> Stats:
        # calcule les stats cumules de tout les equipements
        return reduce(operator.add, [item.stats for item in self.items], Stats())

    def get_stats(self) -> Stats:
        # calcule les stats du billy + son equipement le tout avec les limites des regles
        stats = self.get_items_stats() + self.base_stats
        stats.adr = min(stats.adr, 5)
        return stats

    def get_kind(self) -> BillyKind:
        # retourne la classe du billy en fontion de son equipement
        weapons = 0
        tools = 0
        equipements = 0
        for item in self.items:
            if isinstance(item, Weapon):
                weapons += 1
            elif isinstance(item, Tool):
                tools += 1
            elif isinstance(item, Equipment):
                equipements += 1

        if weapons >= 2:
            return BillyKind.WARRIOR
        if equipements >= 2:
            return BillyKind.CAREFULL
        if tools >= 2:
            return BillyKind.PEASANT
        return BillyKind.DEBROUILLARD

    def compute_damage_with_armor(self, damages: int, modifier: Stats, extra_damages: int = 0) -> int:
        damages = super().compute_damage_with_armor(damages, modifier, extra_damages)
        # peasants are strong, never take more than 3 damages
        if self.kind == BillyKind.PEASANT:
            damages = 3
        return damages

    def roll_dice(self) -> int:
        return randint(1, 6)

    def obtain(self, item_name: str):
        item = Item(item_name)
        item.kind = ItemKind.OBJECT
        self.objects.append(item)
        print(f'Received objects {item_name}')

    def get_delta_hab(self, enemy: Enemy, modifier: Stats) -> int:
        return self.stats.hab + modifier.hab - enemy.stats.hab

    def get_damage_pair(self, enemy: Enemy, modifier: Stats) -> Tuple[int, int]:
        delta_hab = self.get_delta_hab(enemy, modifier)
        dice_score = self.roll_dice()
        print(f'After rolling a dice, you did {dice_score}')
        damages_to_receives, damages_to_inflict = SITUATION_TABLE[delta_hab][dice_score - 1]
        return damages_to_receives, damages_to_inflict

    def fight(self, enemy: Enemy, modifier: Stats = None) -> None:
        if modifier is None:
            modifier = Stats()
        delta_hab = self.get_delta_hab(enemy, modifier)
        if delta_hab <= -8:
            self.die(enemy, 'it\'s a domination')
            self.raise_for_death()
        if delta_hab >= 8:
            enemy.die(self, 'it\'s a domination')
            return
        self.start_fight(enemy, delta_hab)
        enemy.start_fight(self, delta_hab)

        turn = 0
        while enemy.is_alive() and self.is_alive():
            turn += 1
            self._fight_inner_loop(turn, enemy, modifier)

        self.end_fight(enemy)

    def _fight_inner_loop(self, turn: int, enemy: Enemy, modifier: Stats = None) -> None:
        print(f'--- TURN: {turn} ---')
        # start turn event
        self.start_turn(enemy, turn)
        enemy.start_turn(self, turn)

        # damages calaculation phase
        damages_to_receives, damages_to_inflict = self.get_damage_pair(enemy, modifier)

        # dodge phase
        critical, dodged = self.dodge_with_dex()
        if critical:
            damages_to_inflict, _ = SITUATION_TABLE[self.get_delta_hab(enemy, modifier)][5]
            damages_to_inflict += self.stats.crit
            print(f'{enemy} takes extra damage due to critical counter attack !')
        if critical:
            enemy.take_damages(damages_to_inflict)
        else:
            enemy.take_damages_with_armor(damages_to_inflict, modifier,
                extra_damages=1 if self.kind == BillyKind.WARRIOR else 0)

        if not dodged:
            # taking damages phase
            # if billy dies after killed the enemy, then ignore the last round
            damages = self.compute_damage_with_armor(damages_to_receives, modifier)
            if not enemy.is_alive() and damages > self.hp:
                print('Avoided last deadly hit from dead enemy')
            else:
                self.take_damages(damages)

        # post turn phase
        enemy.end_turn(self, turn)
        self.end_turn(enemy, turn)

    def count_item(self, item_name: str) -> int:
        return reduce(
            lambda count, item: count + (1 if item.name == item_name else 0),
            self.objects + self.items,
            0
        )

    def take_damages(self, damages: int) -> None:
        """Reveive `damages` without taking care of any armor, just applying the damages
        """
        super().take_damages(damages)
        self.raise_for_death()

    def dodge_with_dex(self) -> Tuple[bool, bool]:
        if self.stats.adr < 2:
            return (False, False)
        dice = self.roll_dice()
        dodged = dice <= self.stats.adr
        critical = dice == 1
        print(f'Dodge tentative, {dice}! you {"succeded" if dodged else "Failed"}')
        return (critical, dodged)

    def raise_for_death(self):
        """raises `DeathExeption` if billy is dead
        """
        if not self.is_alive():
            raise DeathException

    def get_fight_win_probably_against(self, enemy: Enemy, modifier: Stats,
                                       attemps: int = 10000) -> float:
        """Return the probablity to win against the given `enemy` and `modifier`,
        from 0 (no way) to 1 (definitly win!)
        """
        if attemps <= 0:
            raise ValueError(attemps)
        wins, looses = 0, 0
        billy_hp = self.hp
        enemy_hp = enemy.hp
        with redirect_stdout(None):
            for _ in range(attemps):
                try:
                    self.fight(enemy, modifier)
                    wins += 1
                except DeathException:
                    looses += 1
                finally:
                    self.hp = billy_hp
                    enemy.hp = enemy_hp
        return (looses - wins) / attemps

    def start_fight(self, enemy: "Entity", delta_hability: int) -> None:
        print(f'You enter a fight against {enemy} with {self.hp}hp left')

    def end_fight(self, enemy: "Entity") -> None:
        print(f'After the fight against {enemy}, you have {self.hp} hp left.')
