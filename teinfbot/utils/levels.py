import math


class LevelsUtils:
    LEVEL_MULTIPLIER = 0.15

    @staticmethod
    def levelFromExp(exp: int):
        if exp == 0:
            return 0

        return int(LevelsUtils.LEVEL_MULTIPLIER * math.sqrt(exp))

    @staticmethod
    def expFromLevel(level: int):
        return int(level * level * (1 / LevelsUtils.LEVEL_MULTIPLIER) * (1 / LevelsUtils.LEVEL_MULTIPLIER))
