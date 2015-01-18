#!/usr/bin/env python3
import unittest
from datetime import datetime, time, timedelta
from decimal import *
from tariff import *

def simpleTariff():
    return Tariff(
        dayRate = Decimal('33.00'),
        nightRate = Decimal('40.00'),
        dayStart = time(6, 0, 0, 0),
        nightStart = time(18, 0, 0, 0)
    )

class Test15Min(unittest.TestCase):
    def test15MinDayWithin(self):
        start = datetime(year=2015, month=1, day=20, hour=10)
        end = start + timedelta(minutes=15)
        self.assertEqual(Decimal('33.00'), simpleTariff().charge(start, end))

    def test15MinDayCrossover(self):
        start = datetime(year=2015, month=1, day=20, hour=17, minute=55)
        end = start + timedelta(minutes=15)
        self.assertEqual(Decimal('40.00'), simpleTariff().charge(start, end))

    def test15MinNightCrossover(self):
        start = datetime(year=2015, month=1, day=20, hour=5, minute=55)
        end = start + timedelta(minutes=15)
        self.assertEqual(Decimal('40.00'), simpleTariff().charge(start,end))

class TestOneHour(unittest.TestCase):
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

class TestOneDay(unittest.TestCase):
    def testOneDayStartEdge(self):
        start = datetime(year=2015, month=1, day=20, hour=6)
        end = start + timedelta(hours = 24)
        self.assertEqual(Decimal('876.00'), simpleTariff().charge(start, end))
    
    def testOneDayEndEdge(self):
        start = datetime(year=2015, month=1, day=20, hour=18)
        end = start + timedelta(hours = 24)
        self.assertEqual(Decimal('876.00'), simpleTariff().charge(start, end))

    def testOneDayCrossover(self):
        start = datetime(year=2015, month=1, day=20, hour=6, minute=1)
        end = start + timedelta(hours = 24)
        self.assertEqual(Decimal('883.00'), simpleTariff().charge(start, end))

class TestMaxHours(unittest.TestCase):
    def testMaxHoursAligned(self):
        start = datetime(year=2015, month=1, day=20, hour=6)
        end = start + timedelta(hours=72)
        self.assertEqual(
            3 * (12*Decimal('33.00') + 12*Decimal('40.00')),
            simpleTariff().charge(start, end)
        )

    def testMaxHoursSkewed(self):
        start = datetime(year=2015, month=1, day=20, hour=6, minute=30)
        end = start + timedelta(hours=72)
        self.assertEqual(
            3 * (11*Decimal('33.00') + 13*Decimal('40.00')),
            simpleTariff().charge(start, end)
        )

class TestOverMaxHours(unittest.TestCase):
    def testOverMaxHoursAligned(self):
        start = datetime(year=2015, month=1, day=20, hour=6)
        end = start + timedelta(hours=73)
        self.assertRaises(
            ExcessiveReservation,
            simpleTariff().charge,
            start,
            end
        )

    def testOverMaxHoursSkewed(self):
        start = datetime(year=2015, month=1, day=20, hour=6, minute=30)
        end = start + timedelta(hours=73)
        self.assertRaises(
            ExcessiveReservation,
            simpleTariff().charge,
            start,
            end
        )

class TestUnderMinHours(unittest.TestCase):
    def testUnderMinHoursAligned(self):
        start = datetime(year=2015, month=1, day=20, hour=6)
        end = start + timedelta(minutes=14)
        self.assertRaises(
            DwarfishReservation,
            simpleTariff().charge,
            start,
            end
        )

    def testUnderMinHoursSkewed1(self):
        start = datetime(year=2015, month=1, day=20, hour=6, minute=30)
        end = start + timedelta(minutes=14)
        self.assertRaises(
            DwarfishReservation,
            simpleTariff().charge,
            start,
            end
        )

    def testUnderMinHoursSkewed2(self):
        start = datetime(year=2015, month=1, day=20, hour=6, minute=55)
        end = start + timedelta(minutes=14)
        self.assertRaises(
            DwarfishReservation,
            simpleTariff().charge,
            start,
            end
        )

if __name__ == '__main__':
    unittest.main()