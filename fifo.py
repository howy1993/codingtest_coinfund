import csv
import collections

# assumption1: dates given in chronological order

class Transaction:
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

class Asset:
    def __init__(self, name):
        self.q = collections.deque()
        self.name = name

    def transact(self, price, amount):
        balance = 0
        if (amount > 0):
            self.q.append(Transaction(price, amount))
            return balance

        #can probably improve logic here for runtime
        while (amount < 0):
            if self.q:
                self.q.append(Transaction(price, 0))
                if (amount > self.q[0].amount):
                    removedtx = self.q.popleft()
                    balance += removedtx.amount * (price - removedtx.price)
                    amount -= removedtx.amount
                else:
                    #signs flipped to account for negative amount
                    self.q[0].amount += amount
                    balance -= amount*(price - self.q[0].price)
                    return balance
            else:
                print("Error: detected sale before purchase (short selling is not supported)")
                return 0

#change so receives filetype
with open('test.csv') as csv_file:
    thisdict = {}
    pnl = 0
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_number_debug = 0
    next(csv_reader)
    for row in csv_reader:
        line_number_debug += 1
        if (row[1] not in thisdict):
            thisdict[row[1]] = Asset(row[1])
        pnl += thisdict[row[1]].transact(int(row[2]), int(row[3]))

print("pnl is:", pnl)
#portfolio value
for x in thisdict:
    total_amount = 0
    for y in thisdict[x].q:
        total_amount += y.amount
    print(thisdict[x].name, total_amount, thisdict[x].q[-1].price)
