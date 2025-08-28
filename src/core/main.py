from Pendulum import Pendulum
import sim
import numpy as np
import time
import matplotlib as mpl


start_time = time.time()

length = 1
angle = np.pi / 3
angularVelocity = 0
interval = 0.0250
g = 9.81

pen = Pendulum(length, angle, angularVelocity)

pos = sim.simulatePendulum(pen, interval, g)
ani = sim.produceAnimation(pen, pos, interval * 1000)

mpl.rcParams['animation.ffmpeg_path'] = (r'E:\\Programs\\ffmpeg'
                                         '\\bin\\ffmpeg.exe')
#ani.save("file.mp4")

print("--- %s seconds ---" % (time.time() - start_time))
