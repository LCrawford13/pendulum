from Pendulum import Pendulum
import numpy as np
import sim
import matplotlib.pyplot as plt

pen = Pendulum()

fat = sim.simulatePendulum(pen)
sim.producePlots(pen, fat)


# plt.plot(1, 2, 'ro')
# plt.ylabel = "FART"
# plt.show()