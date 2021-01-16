import random


class FileUtils:
    @staticmethod
    def getNumberOfLines(f):
        with open(f, "r") as file:
            return sum(1 for line in file)

    @staticmethod
    def getRandomLine(f):
        numOfLines = FileUtils.getNumberOfLines(f)
        randomLine = random.randint(0, numOfLines-1)
        with open(f, "r") as file:
            for i in range(randomLine):
                next(file)
            return next(file).rstrip()
