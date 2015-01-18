#!/usr/bin/env python3
import unittest
from datetime import datetime, time, timedelta
from decimal import *
from tariff import Tariff

def simpleTariff():
    return Tariff(
        dayRate = Decimal('33.00'),
        nightRate = Decimal('40.00'),
        dayStart = time(6, 0, 0, 0),
        nightStart = time(18, 0, 0, 0)
    )

class TestCharge(unittest.TestCase):
    def testOneHourDayNormal(self):
        start = datetime(year=2015, month=1, day=20, hour=10)
        end = start + timedelta(hours=1)
        self.assertEqual(Decimal('33.00'), simpleTariff().charge(start, end))

    def testOneHourDayStartEdge(self):
        start = datetime(year=2015, month=1, day=20, hour=6)
        end = start + timedelta(hours=1)
        self.assertEqual(Decimal('33.00'), simpleTariff().charge(start, end))

    def testOneHourDayEndEdge(self):
        end = datetime(year=2015, month=1, day=20, hour=18)
        start = end - timedelta(hours=1)
        self.assertEqual(Decimal('33.00'), simpleTariff().charge(start, end))

    def testOneHourNightNormal(self):
        start = datetime(year=2015, month=1, day=20, hour=20)
        end = start + timedelta(hours=1)
        self.assertEqual(Decimal('40.00'), simpleTariff().charge(start, end))

    def testOneHourNightStartEdge(self):
        start = datetime(year=2015, month=1, day=20, hour=18)
        end = start + timedelta(hours=1)
        self.assertEqual(Decimal('40.00'), simpleTariff().charge(start, end))

    def testOneHourNightEndEdge(self):
        end = datetime(year=2015, month=1, day=20, hour=6)
        start = end - timedelta(hours=1)
        self.assertEqual(Decimal('40.00'), simpleTariff().charge(start, end))

if __name__ == '__main__':
    unittest.main()