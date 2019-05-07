import csv
import sys
import collections
from decimal import *

# assumption1: dates given in chronological order

class Transaction:
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

class Asset:
    def __init__(self, name):
        self.q = collections.deque()
        self.name = name

    def buy(self, price, amount):
        self.q.append(Transaction(price, amount))

    def sell(self, price, amount):
        balance = 0
        #can probably improve logic here for runtime
        while (amount < 0):
            if self.q:
                if (-amount > self.q[0].amount):
                    removedtx = self.q.popleft()
                    balance += removedtx.amount * (price - removedtx.price)
                    amount += removedtx.amount
                else:
                    #signs flipped to account for negative amount
                    self.q[0].amount += amount
                    balance -= amount*(price - self.q[0].price)
                    self.q.append(Transaction(price, 0))
                    return balance
            else:
                print("Error: detected sale before purchase (short selling is not supported)")
                exit()

with open(sys.argv[1], 'r') as csv_file:
    thisdict = {}
    pnldict = {}
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_number_debug = 0
    totalpnl = 0
    totalassets = 0
    next(csv_reader)
    for row in csv_reader:
        line_number_debug += 1
        if (row[1] not in thisdict):
            thisdict[row[1]] = Asset(row[1])
        if (Decimal(row[3]) > 0):
            thisdict[row[1]].buy(Decimal(row[2]), Decimal(row[3]))
        else:
            if (row[1] not in pnldict):
                pnldict[row[1]] = 0
            pnldict[row[1]] += thisdict[row[1]].sell(Decimal(row[2]), Decimal(row[3]))

#Printing Portfolio Value
for x in thisdict:
    for y in thisdict[x].q:
        total_amount = 0
        for y in thisdict[x].q:
            total_amount += y.amount
    if (total_amount != 0):
        totalassets+=1
print("Portfolio: ({0} assets)".format(totalassets))
for x in thisdict:
    total_amount = 0
    for y in thisdict[x].q:
        total_amount += y.amount
    if (total_amount != 0):
        print("{0}: {1} ${2}".format(thisdict[x].name, total_amount, total_amount*thisdict[x].q[-1].price))

#Printing PnL
print("Portfolio: ({0} assets)".format(len(pnldict)))
for x in pnldict:
    neg = ""
    if (pnldict[x] < 0):
        neg = "-"
    print("{2}: {1}${0}".format(abs(pnldict[x]),neg, x))
    totalpnl += pnldict[x]
neg = ""
if (totalpnl < 0):
    neg = "-"
print("Total P&L: {1}${0}".format(abs(totalpnl),neg))
