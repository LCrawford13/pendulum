import matplotlib.pyplot as plt
import numpy as np

def RungeKutta(func, h, oldState, consts, *args):
    a = func(consts, *args)
    b = func(consts + h/2, *args + a*h/2)
    c = func(consts + h/2, *args + b*h/2)
    d = func(consts, *args + c*h)
    
    newState = oldState + (a + 2*b + 2*c + d)*h/6
    
    return newState


def equ(t, y):
    return y * np.square(np.sin(t))

y = [1]
times = np.linspace(0, 5, 60, retstep = True)
t = times[0]
steps = times[1]

for i in range(1, len(t)):
    y.append(RungeKutta(equ, steps, y[i - 1], t[i - 1], y[i - 1]))


fig, ax = plt.subplots()

ax.plot(t, y, color = 'red')

t2 = np.linspace(0, 5, 60)
#y2 = 1*np.exp(1 - np.cos(t2))
y2 = 1*np.exp(0.5 * ( t - 0.5 * np.sin(2 * t)))

ax.plot(t2, y2)
