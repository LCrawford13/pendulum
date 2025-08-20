import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def RungeKutta(func, h, oldState, consts, *args):
    a = func(consts, *args)
    b = func(consts, *args + a*h/2)
    c = func(consts, *args + b*h/2)
    d = func(consts, *args + c*h)
    
    newState = oldState + (a + 2*b + 2*c + d)*h/6
    
    return newState

def dESimplePendulum(consts, angle):
    return -np.sin(angle) * consts[0]/consts[1]

def simulatePendulum(pendulum, frames = 60, intervalTime = 0.1, g = 9.81):
    positions = [[pendulum.massCoor[0]], [pendulum.massCoor[1]]]
    initialAngle = np.tan(pendulum.massCoor[0]/pendulum.massCoor[1])
    time = 0
    initialAngle = -np.pi/2
    for i in range(1, frames):
        angle = RungeKutta(dESimplePendulum, intervalTime, initialAngle,
                           [g, pendulum.length], initialAngle)
        #angle = initialAngle * np.cos(time * np.sqrt(g/pendulum.length))
        
        #angle = (time - intervalTime) * np.sqrt(g / pendulum.length) - initialAngle
        initialAngle = np.copy(angle)

        if positions[0][i - 1] > 0 and positions[1][i - 1] > 0:
            x = pendulum.length * np.sin(angle)
            y = pendulum.length * np.cos(angle)
        elif positions[0][i - 1] < 0 and positions[1][i - 1] > 0:
            x = pendulum.length * np.cos(angle)
            y = pendulum.length * np.sin(angle)
        elif positions[0][0] > 0 and positions[0][1] < 0:
            x = pendulum.length * np.cos(angle)
            y = pendulum.length * np.sin(angle)
        else:
            x = pendulum.length * np.cos(angle)
            y = pendulum.length * np.sin(angle)
        x = pendulum.length * np.sin(angle)
        y = pendulum.length * np.cos(angle)
        print(x)
        positions[0].append(x)
        positions[1].append(y)
        
        # Designed for if there is air resistance, but this method can't
        # calculate air resistance.
        # if len(positions) > 9:
        #     recent = positions[-10:]
        #     unique = np.unique(recent, axis = 0)
        #     if len(unique) == 1:
        #         changing = False

        time += intervalTime

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
    

