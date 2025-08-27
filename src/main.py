from Pendulum import Pendulum
import sim
import numpy as np
import time

start_time = time.time()

length = 10
angle = np.pi / 2
angularVelocity = 0
interval = 0.0250
g = 9.81

pen = Pendulum(length, angle, angularVelocity)

pos = sim.simulatePendulum(pen, interval, g)
ani = sim.produceAnimation(pen, pos, interval * 1000)

print("--- %s seconds ---" % (time.time() - start_time))
