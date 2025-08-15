import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.animation as an

def simulatePendulum(pendulum, t = 0.01, g = 9.81):
    positions = [[pendulum.massCoor[0], pendulum.massCoor[1]]]
    
    changing = True
    while changing:
        angle = t * np.sqrt(g / pendulum.length)
        x = pendulum.length * np.cos(angle)
        y = pendulum.length * np.sin(angle)
        
        positions.append([x, y])
        
        # if len(positions) > 9:
        #     recent = positions[-10:]
        #     unique = np.unique(recent, axis = 0)
        #     if len(unique) == 1:
        #         changing = False
        
        if len(positions) > 1:
            changing = False
        else:
            t += t
            
    return positions

def producePlots(pendulum, positions):
    i = 0
    for points in positions:
        plt.figure(i, figsize = (5, 5))
        plt.plot(points[0], points[1], 'ro')
        plt.plot([points[0], pendulum.pendCoor[0]], 
                 [points[1], pendulum.pendCoor[1]],
                 color = 'r', linestyle = '-')
        
        m = int(pendulum.length + 0.2*pendulum.length)
        plt.xlim(-m, m)
        plt.ylim(-m, m)
        i += 1
        
    plt.show()
    

