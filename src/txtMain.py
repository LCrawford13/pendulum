from Pendulum import Pendulum
import sim
import numpy as np
import matplotlib as mpl
import userpaths
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# This file contains a text-based user interface, it's now obsolete, aside for
# testing purposes.

length = 1
angle = -np.pi / 2
angularVelocity = 0
interval = 0.0125
g = -9.81
pendCoor = np.array([0, 0])


def inputVal(name, value):
    valueTemp = input(f"Would you like to change the {name}? "
                      f"The default value is {value} (SI units), "
                      "press enter to use the default value.")
    if valueTemp != "":
        return valueTemp
    else:
        return value


# Allows user to edit values in the editor instead of using the text-based
# interface.
textInterface = False
if textInterface:
    correctInputs = False
    while not correctInputs:
        length = inputVal("length of the pendulum", length)
        angle = inputVal("initial angle of the pendulum", angle)
        angularVelocity = inputVal("initial angular velocity of the pendulum",
                                   angularVelocity)
        interval = inputVal("time interval between calculations", interval)
        g = inputVal("gravitational acceleration", g)
        pendCoor = inputVal("coordinates of the pendulum's pivot", pendCoor)

        try:
            pen = Pendulum(length, angle, angularVelocity, pendCoor)
            correctInputs = True
        except Exception as e:
            print(str(e) + "\nPlease try again.")

    save = input("Would you like to save the animation? If so, type "
                 "filepath\\\\filename.mp4, otherwise press enter.")
else:
    pen = Pendulum(length, angle, angularVelocity, pendCoor)
    save = "file.mp4"

pos = sim.simulatePendulum(pen, interval, g)
ani = sim.produceAnimation(pen, pos, interval * 1000)

if save != "":
    filepath = userpaths.get_my_documents() + "\\Pendulum"
    # If file doesn't exsist create it, else do nothing.
    try:
        os.mkdir(filepath)
    except FileExistsError:
        pass

    file = open(filepath + "\\settings.ini", "a+")
    # Sets pointer to start of file.
    file.seek(0)
    line = file.readline()

    if line != "":
        # User has previously entered in the file path.
        setting = line.split(" = ")
        mpeg = setting[1]
    else:
        # User has never entered in the file path.
        mpeg = input("Type in the file path to ffmpeg.exe, in the format "
                     "filepath\\\\ffmpeg.exe ")
        file.write("ffmpegPath = " + mpeg)
    file.close()

    mpl.rcParams['animation.ffmpeg_path'] = (mpeg)
    ani.save(save)

plt.show()
