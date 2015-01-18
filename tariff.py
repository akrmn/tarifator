from datetime import date, datetime, time, timedelta
from decimal import *
ONE_HOUR = timedelta(hours=1)

class NegativeTariff(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NonsenseTariff(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DwarfishReservation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ExcessiveReservation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Tariff:
    def __init__(self,
        dayRate,
        nightRate,
        dayStart = time(6, 0, 0, 0),
        nightStart = time(18, 0, 0, 0)
    ):
        if not (dayRate > 0 and nightRate > 0):
            raise NegativeTariff((dayRate, nightRate))
        if not (
            nightStart.microsecond + 1000000*(
                nightStart.second + 60*(
                    nightStart.minute + 60*(
                        nightStart.hour
                    )
                )
            ) -
            dayStart.microsecond + 1000000*(
                dayStart.second + 60*(
                    dayStart.minute + 60*(
                        dayStart.hour
                    )
                )
            ) >
            60*60*1000000
        ):
            raise NonsenseTariff("")
        self.dayRate = dayRate
        self.nightRate = nightRate
        self.dayStart = dayStart
        self.nightStart = nightStart

    def charge(self, start, end):
        if not (end - start >= timedelta(minutes=15)):
            raise DwarfishReservation(end-start)
        if not (end - start <= timedelta(hours=72)):
            raise ExcessiveReservation(end-start)

        total = Decimal('0.00')
        current = start
        while(current < end):
            dayStart = datetime.combine(current.date(), self.dayStart)
            nightStart = datetime.combine(current.date(), self.nightStart)
            if current < dayStart:
                if current + ONE_HOUR <= dayStart:
                    total = total + self.nightRate
                else:
                    total = total + max(self.dayRate, self.nightRate)
            elif current < nightStart:
                if current + ONE_HOUR <= nightStart:
                    total = total + self.dayRate
                else:
                    total = total + max(self.dayRate, self.nightRate)
            else:
                total = total + self.nightRate
            current = current + ONE_HOUR
        return(total)
