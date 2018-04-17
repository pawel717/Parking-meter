import time, datetime, math

class ParkTime:

    def __init__(self, inDate, outDate):
        self.inDate = inDate
        self.outDate = outDate
        self.parse()

    def parse(self):
        self._totalPrice = 0
        self.minutes = 0
        self.firstHour = 0
        self.hours = 0
        self.days = 0
        self.twoDays = 0
        self.weeks = 0
        self.months = 0
        self.minutes = math.ceil((self.outDate - self.inDate).seconds / 60)  # zaokragla w góre wiec 0.1 to 1
        self.days = (self.outDate - self.inDate).days

        while self.minutes > 60:  # godziny
            self._totalPrice += 4
            self.minutes -= 60
            self.hours += 1

        if self.hours == 23 and self.minutes == 60:  # godz 24 to dodaj dzien
            self.days += 1
            self.hours = 0
            self.minutes -= 60

        if self.minutes > 0:  # pierwsze godziny
            self._totalPrice += 2
            self.firstHour = 1

        while self.days >= 28:  # miesiac
            self.days -= 28
            self.months += 1
            self._totalPrice += 7500

        while self.days >= 7:  # tydzien
            self.days -= 7
            self.weeks += 1
            self._totalPrice += 1800

        while self.days >= 2:  # 48h
            self.days -= 2
            self.twoDays += 1
            self._totalPrice += 250

        daysCount = self.days # 24h
        while daysCount > 0:
            daysCount -= 1
            self._totalPrice += 100

    def getTotalPrice(self):
        return self._totalPrice