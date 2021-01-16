import math


class LevelsUtils:
    LEVEL_MULTIPLIER = 0.5

    @staticmethod
    def levelFromExp(exp: int):
        return int(LevelsUtils.LEVEL_MULTIPLIER * math.sqrt(exp))

    @staticmethod
    def expFromLevel(level: int):
        return (level ** 2) // (LevelsUtils.LEVEL_MULTIPLIER ** 2)
