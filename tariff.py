from datetime import date, datetime, time, timedelta
from decimal import *
ONE_HOUR = timedelta(hours=1)

class Tariff:
    def __init__(self,
        dayRate,
        nightRate,
        dayStart = time(6, 0, 0, 0),
        nightStart = time(18, 0, 0, 0)
    ):
        assert(dayRate > 0 and nightRate > 0)
        assert(
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
        )
        # assert(nightStart - dayStart > timedelta(hours = 1))
        self.dayRate = dayRate
        self.nightRate = nightRate
        self.dayStart = dayStart
        self.nightStart = nightStart

    def charge(self, start, end):
        assert(end - start >= timedelta(minutes=15))
        assert(end - start <= timedelta(hours=72))

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



    # def calcularMonto(self,fi,ff):
    #     reserva = ff-fi

    #     # Assert para verificar que las fechas son validas
    #     assert(259200 >= reserva.days*24*60*60 + reserva.seconds >= 900)

    #     totalHoras = reserva.days*24+reserva.seconds/3600
    #     minutos = (reserva.seconds%3600)/60
    #     print(reserva.days, reserva.seconds)
    #     horasNoche = 0
    #     horasDia   = 0
    #     while(totalHoras > 0):
    #         if(fi.hour >= 6 and fi.hour < 18):
    #             diferencia = 18 - fi.hour if 18 - fi.hour < totalHoras else totalHoras
    #             horasDia += diferencia
    #         elif (fi.hour >= 18):
    #             diferencia = 24 - fi.hour if 24 - fi.hour < totalHoras else totalHoras
    #             horasNoche += diferencia
    #         else:
    #             diferencia = 6 - fi.hour if 6 - fi.hour < totalHoras else totalHoras
    #             horasNoche += diferencia

    #         totalHoras -= diferencia
    #         fi = fi + timedelta(hours = (diferencia))

    #     monto = horasDia*self.tarifaDia + horasNoche*self.tarifaNoche
    #     if((fi.hour == 5 and fi.minute + minutos > 59) or
    #         (fi.hour == 17 and fi.minute + minutos > 59)):
    #         monto += self.tarifaDia if self.tarifaDia > self.tarifaNoche else self.tarifaNoche
    #     elif(fi.minute + minutos > 0) :
    #          monto += self.tarifaDia if self.tarifaDia < self.tarifaNoche else self.tarifaNoche
    #     print(horasDia,"dia")
    #     print(horasNoche,"noche")
    #     return monto
