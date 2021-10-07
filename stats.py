from dataclasses import dataclass


@dataclass
class Stats:
    hab: int
    end: int
    cha: int
    deg: int
    crit: int
    arm: int
    adr: int

    def __init__(self,
                hab: int = 0, end: int = 0, adr: int = 0,
                cha: int = 0, deg: int = 0, crit=0, arm: int = 0) -> None:
        self.hab = hab
        self.end = end
        self.adr = adr
        self.cha = cha
        self.deg = deg
        self.crit = crit
        self.arm = arm

    def __add__(self, other: 'Stats'):
        fields = ('hab', 'end', 'adr', 'cha', 'deg', 'crit', 'arm')
        data = {field: getattr(self, field) + getattr(other, field) for field in fields}
        return Stats(**data)
