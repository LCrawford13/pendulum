from PyQt5 import QtWidgets, QtCore
from gui import MainWindow

import sys


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,
                                        True)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    app.exec_()
