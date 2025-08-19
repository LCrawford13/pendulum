from Pendulum import Pendulum
import numpy as np
import sim
import matplotlib.pyplot as plt

pen = Pendulum()

f = 30



fat = sim.simulatePendulum(pen, frames = f)
ani = sim.produceAnimation(pen, fat, frames = f)

# plt.plot(1, 2, 'ro')
# plt.ylabel = "FART"
# plt.show()
