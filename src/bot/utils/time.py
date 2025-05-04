from datetime import timedelta


def getTimeDescFromMinutes(minutes: int):
    delta = timedelta(minutes=minutes)
    deltaStr = str(delta).replace("days", "dni").replace("day", "dzień")[:-3]
    return deltaStr
