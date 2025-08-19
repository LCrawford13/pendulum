import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def RungeKutta(func, args):
    newState = func()

def dESimplePendulum(length, angle, g = 9.81):
    return -np.sin(angle) * g/length

def simulatePendulum(pendulum, frames = 60, t = 0.01, g = 9.81):
    positions = [[pendulum.massCoor[0]], [pendulum.massCoor[1]]]
    #initialAngle = np.tan(pendulum.massCoor[0]/pendulum.massCoor[1])
    
    initialAngle = np.pi/2
    for i in range(1, frames):
        
        
        angle = initialAngle * np.cos(t * np.sqrt(g/pendulum.length))
        initialAngle = np.copy(angle)
        
        #angle = t * np.sqrt(g / pendulum.length) - initialAngle

        # if positions[0][i - 1] > 0 and positions[1][i - 1] > 0:
        #     angle -= np.pi
        # elif positions[0][i - 1] <= 0 and positions[1][i - 1] > 0:
        #     angle = np.pi - angle
        # elif positions[0][0] > 0 and positions[0][1] <= 0:
        #     angle = 2*np.pi - angle
            
        x = pendulum.length * np.sin(angle)
        y = pendulum.length * np.cos(angle)

        positions[0].append(x)
        positions[1].append(y)
        
        # Designed for if there is air resistance, but this method can't
        # calculate air resistance.
        # if len(positions) > 9:
        #     recent = positions[-10:]
        #     unique = np.unique(recent, axis = 0)
        #     if len(unique) == 1:
        #         changing = False
        
        t += t

    return positions

def produceAnimation(pendulum, positions, frames = 60):
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
    
    ani = animation.FuncAnimation(fig = fig, func = update, frames = frames)
    plt.show()
    
    return ani
    

