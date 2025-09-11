from PyQt5 import QtWidgets, QtCore
from gui import MainWindow

import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    window = MainWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    app.exec_()
