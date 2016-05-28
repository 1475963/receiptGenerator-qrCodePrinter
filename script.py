import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

DUMP_PICFILE = "test.png"
DEFAULT_PICFILE = "placeholder.png"
BTN_LABEL = "Generate"
BTN_TOOLTIP = "This button generates a receipt and prints its qrcode"

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
        self.setWindowTitle('E-Receipts QrCode utility')
        self.show()

    def generateReceipt(self):
        self.receipt = sys.argv[1]
        self.generateQrCode()

    def generateQrCode(self):
        os.system("qr {} > {}".format(self.receipt, DUMP_PICFILE))
        self.picture.swap(QPixmap(DUMP_PICFILE))
        self.label.setPixmap(self.picture)

def main():
    app = QApplication(sys.argv)
    mainWindow = GenerateReceiptPrintQrCode()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
