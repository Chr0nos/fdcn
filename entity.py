from stats import Stats


class Entity:
    name: str
    hp: int
    hp_max: int
    stats: Stats

    def __str__(self):
        return self.name

    def take_damages(self, damages: int) -> None:
        self.hp = max(self.hp - damages, 0)
        print(f'{self} received {damages} damages ({self.hp} hp left)')
        if not self.is_alive():
            print(f'{self} has been killed.')

    def is_alive(self) -> bool:
        return self.hp > 0

    def die(self, killer: 'Entity' = None, reason: str = None) -> None:
        self.hp = 0
        if reason is not None:
            print(f'{self} has been insta-killed by {killer} {reason}')

    def heal(self, hp: int = None) -> None:
        self.hp = min(self.hp + hp, self.hp_max)

    def compute_damage_with_armor(self, damages: int, modifier: Stats, extra_damages: int = 0) -> int:
        """return the amount of damages the Entity will take after applying armor and extra damages
        """
        return max(damages - self.stats.arm - modifier.arm, 0) + extra_damages

    def take_damages_with_armor(self, damages: int, modifier: Stats, extra_damages: int = 0) -> None:
        damages = self.compute_damage_with_armor(damages, modifier, extra_damages)
        self.take_damages(damages)

    def start_fight(self, enemy: "Entity", delta_hability: int) -> None:
        pass

    def start_turn(self, enemy: "Entity", turn_number: int) -> None:
        pass

    def end_turn(self, enemy: "Entity", turn_number: int) -> None:
        pass
