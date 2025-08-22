from Pendulum import Pendulum
import sim
import numpy as np

length = 1
angle = -np.pi/2
angularVelocity = 5
frames = 80*10
interval = 0.0125
g = 9.81

pen = Pendulum(length, angle, angularVelocity)

pos = sim.simulatePendulum(pen, frames, interval, g)
ani = sim.produceAnimation(pen, pos, frames, interval)

ani.save("graph.gif", writer = 'pillow', fps = frames/10)
