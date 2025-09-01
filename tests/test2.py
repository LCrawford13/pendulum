import numpy as np
import matplotlib.pyplot as plt
from Pendulum import Pendulum


# def RungeKutta(func, t, h, oldState, consts, *args):
#     a = func(t, consts, *args)
#     b = func(t + h/2, consts, *args + a*h/2)
#     c = func(t + h/2, consts, *args + b*h/2)
#     d = func(t + h, consts, *args + c*h)
    
#     newState = oldState + (a + 2*b + 2*c + d)*h/6
    
#     return newState

def RungeKutta(func1, func2, h, oldState1, oldState2, consts):
    a1 = func1(consts, oldState1)
    a2 = func2(consts, oldState2)
    
    b1 = func1(consts, oldState1 + a2*h/2)
    b2 = func2(consts, oldState2 + a1*h/2)
    
    c1 = func1(consts, oldState1 + b2*h/2)
    c2 = func2(consts, oldState2 + b1*h/2)
    
    d1 = func1(consts, oldState1 + c2*h)
    d2 = func2(consts, oldState2 + c1*h)
    
    newState1 = oldState1 + (a1 + 2*b1 + 2*c1 + d1)*h/6
    newState2 = oldState2 + (a2 + 2*b2 + 2*c2 + d2)*h/6
    
    return newState1, newState2

def dESimplePendulumAngularVelocity(consts, angle):
    temp = -np.sin(angle) * consts[0]/consts[1]
    return temp

def dESimplePendulumAngle(consts, angularVelocity):
    return angularVelocity

def simulatePendulum(pendulum, frames = 60, intervalTime = 0.1, g = 9.81):
    x = [np.pi/2]
    time = 0
    initialAngle = np.pi/2
    initialAngularVelocity = 50
    for i in range(1, frames):
        angle, angularVelocity = RungeKutta(dESimplePendulumAngularVelocity,
                           dESimplePendulumAngle,
                           intervalTime, initialAngle, 
                           initialAngularVelocity,
                           [g, pendulum.length])
        
        x.append(angle)
        
        initialAngle = np.copy(angle)
        initialAngularVelocity = np.copy(angularVelocity)

    return x


pen = Pendulum()

x = simulatePendulum(pen)
x = np.array(x)
y = (pen.length/9.81) * np.log(np.abs(1/np.sin(x - np.pi/2) + 1/np.tan(x - np.pi/2)))
x2 = np.linspace(-3, 3, 1000)
y2 = (pen.length/9.81) * np.log(np.abs(1/np.sin(x2 - np.pi/2) + 1/np.tan(x2 - np.pi/2)))

x3 = pen.length*np.cos(np.copy(x))
y3 = pen.length*np.sin(np.copy(x))

fig, ax = plt.subplots()

ax.plot(x, y, color = 'red', zorder = 2, label = "Less Fake")
ax.plot(x2, y2, color = 'blue', zorder = 1, label = "Fake")
ax.plot(x3, y3, color = 'green', zorder = 1, label = "RungeKutta")
ax.legend()

