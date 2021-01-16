import math

LEVEL_MULTIPLIER = 0.15


def level_from_exp(exp: int):
    if exp == 0:
        return 0

    return int(LEVEL_MULTIPLIER * math.sqrt(exp))


def exp_from_level(level: int):
    return int(level * level * (1 / LEVEL_MULTIPLIER) * (1 / LEVEL_MULTIPLIER))
