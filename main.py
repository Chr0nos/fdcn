from os import stat
from stats import Stats
from billy import Billy, DeathException
from items import Sword, SacDeGrain, Bow, KitEscalade, Pamphlet
from enemy import Enemy, Massacre
from stats import Stats


if __name__ == "__main__":
    me = Billy(items=[Sword(), Bow(), SacDeGrain()])
    me.path = [
        2, 11, 28, 32, 43, 68, 73, 115, 30, 35, 105, 41,
        14, 67, 137, 90, 277, 124, 237, 22, 12, 100, 79, 279, 289
    ]
    me.obtain('Lettre de recommandation')
    me.obtain('Ecusson d\'orc dechire')

    print(me)

    # putes
    me.mod_stats(Stats(end=1))

    me.goto(122)
    me.goto(138)
    me.mod_stats(Stats(hab=1))
    me.obtain('INFO')

    # le coup!
    me.goto(53)
    me.goto(180)
    me.obtain('INFO')
    me.luck_max += 1

    me.goto(210)
    me.obtain('Fleau rouge fluo a paillettes')
    me.obtain('INFO')

    me.goto(70)
    me.goto(213)
    me.goto(97)

    print(me.__repr__())
    massacre = Massacre()
    # print(me.get_fight_win_probably_against(massacre, Stats(hab=4)))
    try:
        me.fight(massacre, Stats(hab=4))
    except DeathException:
        print('End')


    marie = Billy([Sword(), KitEscalade(), Pamphlet()])
