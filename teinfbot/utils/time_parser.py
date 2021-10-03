from __future__ import annotations


class TimeParser:
    def __init__(self, seconds: int):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.days = days

    @property
    def days_form(self):
        return "dni" if self.days > 1 else "dzień"

    @property
    def hours_form(self):
        return "godzin" if self.hours > 1 else "godzina"

    @property
    def minutes_form(self):
        if self.minutes == 1:
            return "minuta"

        if 2 <= self.minutes <= 4:
            return "minuty"

        return "minut"

    @property
    def seconds_form(self):
        if self.seconds == 1:
            return "sekunda"

        if 2 <= self.seconds <= 4:
            return "sekundy"

        return "sekund"

    @property
    def full_form(self):
        fform = []
        if self.days > 0:
            fform.append(f"{self.days} {self.days_form}")
        if self.hours > 0:
            fform.append(f"{self.hours} {self.hours_form}")
        if self.minutes > 0:
            fform.append(f"{self.minutes} {self.minutes_form}")
        if self.seconds > 0:
            fform.append(f"{self.seconds} {self.seconds_form}")

        return ', '.join(fform)

    def __repr__(self):
        return self.full_form
