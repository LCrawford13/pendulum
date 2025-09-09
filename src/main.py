from PyQt5 import QtWidgets
from gui import MainWindow
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.activateWindow()
    window.raise_()
    app.exec_()
