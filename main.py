from Pendulum import Pendulum
import sim


pen = Pendulum()

f = 80*10
interval = 0.0125


pos = sim.simulatePendulum(pen, frames = f, intervalTime= interval)
ani = sim.produceAnimation(pen, pos, frames = f, interval = interval * 1000)


