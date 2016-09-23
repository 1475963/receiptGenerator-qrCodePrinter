#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import datetime
import math
import binascii
from functools import reduce

USAGE = "./script.py OR python3 script.py WITHOUT ARGUMENTS"
DUMP_PICFILE = "test.png"
DEFAULT_PICFILE = "placeholder.png"
BTN_LABEL = "Generate"
BTN_TOOLTIP = "This button generates a receipt and prints its qrcode"
WINDOW_TITLE = "E-Receipts QrCode utility"

MAX_ITEMS = 10
MAX_PRODUCTS = 4
PRODUCT_NAMES = ["SAC LOUIS VITTON", "COCA-COLA", "SNICKERS",
                 "RAISINS EN GRAPPE", "1664", "GAMING PC MASTER RACE",
                 "PS4", "250 RIOT POINTS", "GUMMY BEARS"]
CURRENCIES = ["EUR", "USD", "GBP"]
PAYMENT_METHODS = ["Credit Card", "Cash", "Cheque"]
COMPANY_NAME = ["Auchan", "Carrefour", "Monoprix", "Franprix", "Primark", "Micromania"]
COMPANY_ADDRESSES = ["blablablabla", "route 64"]
USER_CREDENTIALS = ["bob.sanders/lol154", "fdp999/kek21"]
USER_IDENTITIES = ["bob/sanders/bob.sanders/M", "bob/dylan/fdp999/M"]
USER_ADDRESSES = ["route arc-en-ciel", "deadzone"]

class User():
    
    def __init__(self):
        self.credential = random.choice(USER_CREDENTIALS)
        self.identity = random.choice(USER_IDENTITIES)
        self.address = random.choice(USER_ADDRESSES)

    def __str__(self):
        return (self.credential + "/"
                + self.identity + "/"
                + self.address + "/")

class Company():

    def __init__(self):
        self.name = random.choice(COMPANY_NAME)
        self.address = random.choice(COMPANY_ADDRESSES)
        self.employeeNumber = random.randint(0, 10000)
        self.depth = 1
        self.parent = ""
        self.children = []

    def __str__(self):
        return (self.name + "/"
                + self.address + "/"
                + "Paris/75012/" + hex(int("0145464948"))[2:])

class Product():
    
    def __init__(self):
        self.name = random.choice(PRODUCT_NAMES)
        self.quantity = random.randint(1, MAX_PRODUCTS)
        self.price = random.random() * 100

    def __str__(self):
        return (str(self.quantity) + "|"
                + self.name + "|"
                + "{:.2f}".format(self.price))

    def __add__(self, other):
        return (self.price * self.quantity) + (other.price * other.quantity)

class Receipt():

    def __init__(self):
        self.user = User()
        self.company = Company()
        self.date = datetime.datetime.now()
        self.cart = []
        for i in range(0, random.randint(1, MAX_ITEMS)):
            self.cart.append(Product())
        self.paymentMethod = random.choice(PAYMENT_METHODS)
        self.totalPrice = sum([(product.price * product.quantity) for product in self.cart])
        self.change = -(math.ceil(self.totalPrice) - self.totalPrice + random.randint(0, 100))
        self.currency = random.choice(CURRENCIES)

    def __str__(self):
        res = (str(self.company) + "/"
                + "01062016123045" + "/"
                + "{:.2f}".format(self.change) + "/"
                + self.paymentMethod + "/")
        for i, product in enumerate(self.cart):
            res += str(product)
            if (i < len(self.cart) - 1):
                res += "/"
        return res

class GenerateReceiptPrintQrCode(QWidget):

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.btn = QPushButton(BTN_LABEL, self)
        self.btn.setToolTip(BTN_TOOLTIP)
        self.btn.clicked.connect(self.generateReceipt)
        self.btn.move(60, 8)
        self.label = QLabel("", self)
        self.label.move(0, 50)
        self.label.resize(200, 200)
        self.label.setScaledContents(True)
        self.label.show()
        self.picture = QPixmap(DEFAULT_PICFILE)
        self.label.setPixmap(self.picture)
        self.setGeometry(100, 100, 200, 250)
        self.setWindowTitle(WINDOW_TITLE)
        self.show()

    def generateReceipt(self):
        self.receipt = Receipt()
        self.generateQrCode()

    def generateQrCode(self):
        receiptRepr = "avc"# + '"' + str(self.receipt) + '"aa'
        print("alo: ", receiptRepr)
        os.system("qr {} > {}".format(str(self.receipt), DUMP_PICFILE))
        self.picture.swap(QPixmap(DUMP_PICFILE))
        self.label.setPixmap(self.picture)

def main():
    receipt = Receipt()
    receiptRepr = '"' + str(receipt) + '"'
    print(receiptRepr)
    os.system("qr {} > {}".format(receiptRepr, DUMP_PICFILE))
    """
    app = QApplication(sys.argv)
    mainWindow = GenerateReceiptPrintQrCode()
    sys.exit(app.exec_())
    """

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        print(USAGE)
