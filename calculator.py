#!/usr/bin/env python3
from decimal import *
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

if __name__ == '__main__':
    t = getTariff()
    while True:
