import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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
    positions = [[pendulum.massCoor[0]], [pendulum.massCoor[1]]]
    initialAngle = np.pi/2
    initialAngularVelocity = 0
    for i in range(0, frames):
        angle, angularVelocity = RungeKutta(dESimplePendulumAngularVelocity,
                           dESimplePendulumAngle,
                           intervalTime, initialAngle, 
                           initialAngularVelocity,
                           [g, pendulum.length])
        print(angularVelocity)
        

        # if positions[0][i - 1] > 0 and positions[1][i - 1] > 0:
        #     x = pendulum.length * np.sin(angle)
        #     y = pendulum.length * np.cos(angle)
        # elif positions[0][i - 1] < 0 and positions[1][i - 1] > 0:
        #     x = pendulum.length * np.cos(angle)
        #     y = pendulum.length * np.sin(angle)
        # elif positions[0][0] > 0 and positions[0][1] < 0:
        #     x = pendulum.length * np.cos(angle)
        #     y = pendulum.length * np.sin(angle)
        # else:
        #     x = pendulum.length * np.cos(angle)
        #     y = pendulum.length * np.sin(angle)
        x = pendulum.length * np.cos(angle)
        y = pendulum.length * np.sin(angle)

        initialAngle = np.copy(angle)
        initialAngularVelocity = np.copy(angularVelocity)
        
        positions[0].append(x)
        positions[1].append(y)
        
        # Designed for if there is air resistance, but this method can't
        # calculate air resistance.
        # if len(positions) > 9:
        #     recent = positions[-10:]
        #     unique = np.unique(recent, axis = 0)
        #     if len(unique) == 1:
        #         changing = False


    return positions

def produceAnimation(pendulum, positions, frames = 60, interval = 100):
    fig, ax = plt.subplots()

    m = int(pendulum.length + 0.2*pendulum.length)

    def update(frame):
        ax.clear()
        
        ax.scatter(positions[0][frame], positions[1][frame], 
                   color = 'black', zorder = 2)
        ax.plot([positions[0][frame], pendulum.pendCoor[0]],
                  [positions[1][frame], pendulum.pendCoor[1]],
                  color = 'brown', linestyle = '-', zorder = 1)
        
        plt.xlim(-m, m)
        plt.ylim(-m, m)
    
    ani = animation.FuncAnimation(fig = fig, func = update,
                                  frames = frames, interval = interval)
    plt.show()
    
    return ani
    

