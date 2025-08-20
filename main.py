from Pendulum import Pendulum
import numpy as np
import sim
import matplotlib.pyplot as plt

pen = Pendulum()

f = 80*10
interval = 0.0125


pos = sim.simulatePendulum(pen, frames = f, intervalTime= interval)
ani = sim.produceAnimation(pen, pos, frames = f, interval = interval * 1000)


