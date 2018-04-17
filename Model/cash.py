class Cash:
    def __init__(self, value):
        if self.checkIfAllowed(value):
            self._value = value
        else:
            print("Niedozwolona wartosc")
            self._value = 0

    def checkIfAllowed(self, value):
        for i in self.allowedValues:
            if value == i:
                return 1
        else:
            return 0

    def getValue(self):
        return self._value

class CoinZl(Cash):
    def __init__(self, value):
        self.allowedValues = [1, 2, 5]
        Cash.__init__(self, value)

class CoinGr(Cash):
    def __init__(self, value):
        self.allowedValues = [1, 2, 5, 10, 20, 50]
        Cash.__init__(self, value)

class Bill(Cash):
    def __init__(self, value):
        self.allowedValues = [10, 20, 50, 100, 200]
        Cash.__init__(self, value)

class Total:
    def __init__(self):
        self._cashListZl = []
        self._cashListGr = []

    def get_total(self):
        sumGr = 0
        sumZl = 0
        for i in self._cashListGr:
            sumGr += i.getValue()
        for i in self._cashListZl:
            sumZl += i.getValue()
        return round(sumZl + sumGr / 100, 2)

    def add(self, cash):
        if isinstance(cash, CoinGr):
            self._cashListGr.append(cash)
        else:
            self._cashListZl.append(cash)

    def giveChange(self, total, change):
        self._cashListGr.sort(key= lambda x: x.getValue(), reverse=True)
        self._cashListZl.sort(key= lambda x: x.getValue(), reverse=True)
        cashListGr=self._cashListGr[:]
        cashListZl=self._cashListZl[:]
        for x in self._cashListZl:
            if change<=0:
                break
            if change>=x.getValue():
                change-=x.getValue()
                cashListZl.remove(x)

        change*=100
        for x in self._cashListGr:
            if change<=0:
                break
            if change>=x.getValue():
                change-=x.getValue()
                cashListGr.remove(x)

        if change==0:
            self._cashListGr=cashListGr+total._cashListGr
            self._cashListZl=cashListZl+total._cashListZl
            return True
        else:
            return False

    def removeAll(self):
        self.__init__()