#!/usr/bin/env python3
from decimal import *
from datetime import datetime
from tariff import Tariff
TWOPLACES = Decimal(10) ** -2

def getTariff():
    done = 'n'
    while done[0] != 'y' and done[0] != 'Y':
        dayRate = Decimal(
            input("enter the day rate (ex: 123.99) > ")
        ).quantize(TWOPLACES)
        nightRate = Decimal(
            input("enter the night rate (ex: 123.99) > ")
        ).quantize(TWOPLACES)

        t = Tariff(dayRate, nightRate)

        print("Day:   From 06:00 to 18:00, {0}".format(t.dayRate))
        print("Night: From 18:00 to 06:00, {0}".format(t.nightRate))
        done = input("Are those rates OK? (y/n) > ")
    return(t)

def getDatetime(moment):
    print("{0} date-time:".format(moment))
    year = int(input("\tenter year (yyyy) > "))
    month = int(input("\tenter month (mm) > "))
    day = int(input("\tenter day (dd) > "))
    hour = int(input("\tenter hour (hh) > "))
    minute = int(input("\tenter minute (mm) > "))
    return(
        datetime(
            year = year,
            month = month,
            day = day,
            hour = hour,
            minute = minute
        )
    )

if __name__ == '__main__':
    t = getTariff()
    while True:
        startDatetime = getDatetime("Start")
        endDatetime = getDatetime("End")
        print(t.charge(startDatetime, endDatetime))
