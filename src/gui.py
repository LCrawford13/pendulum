from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from ui_gui import Ui_MainWindow
from Pendulum import Pendulum
from os import mkdir

import matplotlib as mpl
import numpy as np
import userpaths
import sim

mpl.use('Qt5Agg')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.canvas = FigureCanvasQTAgg(Figure(figsize = (5, 5), dpi = 150))
        self.ui.vLayout.addWidget(self.canvas)

        self.ui.lengthSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.ui.applyButton, True))
        self.ui.gSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.ui.applyButton, True))
        self.ui.angleSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.ui.applyButton, True))
        self.ui.angularVelocitySpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.ui.applyButton, True))
        self.ui.xSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.ui.applyButton, True))
        self.ui.ySpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.ui.applyButton, True))
        self.ui.intervalSpinBox.valueChanged['double'].connect(
            lambda: self.toggleButton(self.ui.applyButton, True))
        self.ui.applyButton.clicked.connect(self.simulate)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.ffmpegButton.clicked.connect(self.changeFfmpegFilePath)

        self.checkFfmpegFilePath()

    def simulate(self):
        """
        Occurs when the user clicks the applyButton, this will generate an
        animation based on the values in the various spin boxes, and then
        display this animation to the user.
        """
        self.toggleButton(self.ui.applyButton, False)
        self.toggleButton(self.ui.saveButton, True)
        self.ui.errorLabel.setText("")

        # Try and except needed in case the user inputs an incorrect value.
        try:
            length = self.ui.lengthSpinBox.value()
            g = self.ui.gSpinBox.value()
            angle = self.ui.angleSpinBox.value() * np.pi
            angularVelocity = self.ui.angularVelocitySpinBox.value()
            pendCoor = [self.ui.xSpinBox.value(), self.ui.ySpinBox.value()]
            interval = self.ui.intervalSpinBox.value()

            pen = Pendulum(length, angle, angularVelocity, pendCoor)
            pos = sim.simulatePendulum(pen, interval, g)

            if hasattr(self, 'ani'):
                self.canvas.figure.clf()
                self.ani.pause()
                # If the user has played more than one animation this session,
                # then the previous animation needs to stop playing.

            ax = self.canvas.figure.add_subplot(111)

            self.ani = sim.produceAnimation(pen, pos, interval * 1000,
                                            self.canvas.figure, ax)

            self.canvas.draw()
        except Exception as e:
            self.ui.errorLabel.setText(str(e))

    def save(self):
        """
        Occurs when the user clicks the saveButton, this will save the
        animation which is currently being shown to the user to an mp4 file,
        the name and location of the file will be given by the user through
        a file dialog window.
        """
        self.ui.errorLabel.setText("")

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
            self.ui.errorLabel.setText(str(e))

    def changeFfmpegFilePath(self):
        """
        Occurs when user clicks ffmpegButton, resulting in a file dialog window
        allowing the user to select the file path to ffmpeg.exe.
        """
        self.ui.errorLabel.setText("")

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
            self.ui.errorLabel.setText(str(e))

    def checkFfmpegFilePath(self, ffmpegFilePath = ""):
        """
        Checks to see if the user has previously set the file path of
        ffmpeg.exe. If they have, then it tells matplotlib the file path.
        Otherwise it creates a settings.ini in the user's my documents.

        Parameters
        ----------
        ffmpegFilePath : String, optional
            If not equal to "", then it means the user has entered the file
            path of ffmpeg, which will then be written into settings.ini.
            The default is "".
        """
        filepath = userpaths.get_my_documents() + "\\Pendulum"

        # If file doesn't exsist create it.
        try:
            mkdir(filepath)
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
        """
        For a subclass of QMainWindow, closeEvent will fire when the subclass
        is closed. In this case, it makes sure that animations based on
        matplotlib are disposed off.
        """
        if hasattr(self, 'ani'):
            self.ani.pause()
            # Stops animations from continuing in background.
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
