import sim
import os
import userpaths
import numpy as np
import matplotlib as mpl
from Pendulum import Pendulum
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import uic

mpl.use('Qt5Agg')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('gui.ui', self)

        self.canvas = FigureCanvasQTAgg(Figure(figsize = (5, 5), dpi = 150))
        self.vLayout.addWidget(self.canvas)

        self.lengthSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.applyButton, True))
        self.gSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.applyButton, True))
        self.angleSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.applyButton, True))
        self.angularVelocitySpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.applyButton, True))
        self.xSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.applyButton, True))
        self.ySpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.applyButton, True))
        self.intervalSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.applyButton, True))
        self.applyButton.clicked.connect(self.simulate)
        self.saveButton.clicked.connect(self.save)
        self.ffmpegButton.clicked.connect(self.changeFfmpegFilePath)

        self.checkFfmpegFilePath()

    def simulate(self):
        self.toggleButton(self.applyButton, False)
        self.toggleButton(self.saveButton, True)

        # Try and except needed in case the user inputs an incorrect value.
        try:
            length = self.lengthSpinBox.value()
            g = self.gSpinBox.value()
            angle = self.angleSpinBox.value() * np.pi
            angularVelocity = self.angularVelocitySpinBox.value()
            pendCoor = [self.xSpinBox.value(), self.ySpinBox.value()]
            interval = self.intervalSpinBox.value()

            pen = Pendulum(length, angle, angularVelocity, pendCoor)
            pos = sim.simulatePendulum(pen, interval, g)

            self.canvas.figure.clf()
            ax = self.canvas.figure.add_subplot(111)

            self.ani = sim.produceAnimation(pen, pos, interval * 1000,
                                            self.canvas.figure, ax)

            self.canvas.draw()
        except Exception as e:
            self.errorLabel.setText(str(e))

    def save(self):
        try:
            if self.setting != "":
                fileDialog = QFileDialog(self)
                fileDialog.setWindowTitle("Save Animation")
                fileDialog.setDefaultSuffix("mp4")
                fileDialog.setAcceptMode(QFileDialog.AcceptSave)
                fileDialog.setNameFilters(['MP4 (*.mp4)'])
                fileDialog.setViewMode(QFileDialog.ViewMode.Detail)

                if fileDialog.exec():
                    selectedFiles = fileDialog.selectedFiles()
                    self.ani.save(selectedFiles[0])
            else:
                raise Exception("Needs file path for ffmpeg.exe.")
        except Exception as e:
            self.errorLabel.setText(str(e))

    def changeFfmpegFilePath(self):
        try:
            fileDialog = QFileDialog(self)
            fileDialog.setWindowTitle("Find ffmpeg")
            fileDialog.setDefaultSuffix("exe")
            fileDialog.setNameFilters(['exe (ffmpeg.exe)'])
            fileDialog.setViewMode(QFileDialog.ViewMode.Detail)

            if fileDialog.exec():
                selectedFiles = fileDialog.selectedFiles()
                self.checkFfmpegFilePath(selectedFiles[0])
        except Exception as e:
            self.errorLabel.setText(str(e))

    def checkFfmpegFilePath(self, ffmpegFilePath = ""):
        filepath = userpaths.get_my_documents() + "\\Pendulum"

        # If file doesn't exsist create it.
        try:
            os.mkdir(filepath)
        except FileExistsError:
            pass

        file = open(filepath + "\\settings.ini", "a+")

        if ffmpegFilePath != "":
            file.write("ffmpegPath = " + ffmpegFilePath)

        # Sets pointer to start of file.
        file.seek(0)
        self.setting = file.readline()

        if self.setting != "":
            filepath = self.setting.split(" = ")[1]
            mpl.rcParams['animation.ffmpeg_path'] = (filepath)

        file.close()

    def closeEvent(self, event):
        self.canvas.figure.clf()

    @staticmethod
    def toggleButton(button, toggle):
        """
        Changes whether the button is enabled or disabled.

        Parameters
        ----------
        button : QPushButton
            The button to enable or disable,
        toggle : Bool
            Determines whether the button is enabled or disabled.
        """
        button.setEnabled(toggle)
