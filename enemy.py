from dataclasses import dataclass

from stats import Stats
from entity import Entity


class Enemy(Entity):
    name = 'Enemy'

    def __init__(self, pv: int, hab: int, dmg: int, armor: int = 0):
        self.hp = pv
        self.hp_max = pv
        self.stats = Stats(hab=hab, arm=armor, deg=dmg)


class Massacre(Enemy):
    name = 'Massacre'

    def __init__(self):
        super().__init__(hab=12, pv=20, dmg=1)

    def start_fight(self, billy: "Entity", delta_hability: int) -> None:
        self.turns_to_kill_billy = 5
        if billy.count_item('INFO') >= 3:
            self.turns_to_kill_billy = 8
        print(f'You have {self.turns_to_kill_billy} turns before being surouded by {self}\'s forces.')

    def end_turn(self, billy, turn_number: int) -> None:
        if not self.is_alive():
            return
        if turn_number % 3 == 0 and turn_number > 1:
            print(f'{self} threw a flame bolt!')
            billy.receive_damages(3)
        if turn_number == self.turns_to_kill_billy:
            billy.die(self, 'after surrounded you with additional forces')
