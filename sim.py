import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl

def RungeKutta(func1, func2, h, oldState1, oldState2, consts):
    """
    Runge Kutta algorithm to find numerical solutions to differential
    equations of a certain form. This implementation is currently a less
    general form of the algorithm, where the differential equation must be of
    the form d(x)/dt = f(x). Constants like g or the lenght of a pendulum, can
    be passed into func1 and func2 via the consts parameter.

    Parameters
    ----------
    func1 : function
        Function to calculate newsState1 from consts and oldState2. Most
        likely, f(x), the differential equation itself.
    func2 : function
        Function to calculate newsState2 from consts and oldState1. Most
        likely, just x.
    h : float
        Time interval over which oldState1 and oldState2 are changing,
        in seconds.
    oldState1 : float
        Most likely x.
    oldState2 : float
        Most likely d(x)/dt.
    consts : list
        List of constants which may want to be changed, for example the length
        of a pendulum. Will be passed into func1 and func2.

    Returns
    -------
    newState1 : float
        Most likely x, after time period h.
    newState2 : TYPE
        Most likely d(x)/dt after time period h.
    """
    a1 = func1(consts, oldState1)
    a2 = func2(consts, oldState2)

    b1 = func1(consts, oldState1 + a2*h/2)
    b2 = func2(consts, oldState2 + a1*h/2)

    c1 = func1(consts, oldState1 + b2*h/2)
    c2 = func2(consts, oldState2 + b1*h/2)

    d1 = func1(consts, oldState1 + c2*h)
    d2 = func2(consts, oldState2 + c1*h)

    newState1 = oldState1 + (a2 + 2*b2 + 2*c2 + d2)*h/6
    newState2 = oldState2 + (a1 + 2*b1 + 2*c1 + d1)*h/6

    return newState1, newState2


def dESimplePendulumAngularVelocity(consts, angle):
    """
    Represents the differential equation for a simple pendulum, the derivate
    of the angle with respect to time, so the angular velocity (omega), equals
    the negative of g divided by the length of the pendulum (L), all
    multiplied by the sine of the angle (theta):
    d(omega)/dt = -sin(theta) * g/L

    Parameters
    ----------
    consts : list
        Holds variables for g and the length of the pendulum, both in SI units.
        g at index 0, and length at index 1.
    angle : float
        The initial angle in radians.

    Returns
    -------
    float
        Returns the new angular velocity.
    """
    return -np.sin(angle) * consts[0]/consts[1]


def dESimplePendulumAngle(consts, angularVelocity):
    """
    Exists purely to allow the RungeKutta function to be more general.

    Parameters
    ----------
    consts : list
        Not used, purely here to make RungeKutta more general.
    angularVelocity : float
        The initial angular velocity.

    Returns
    -------
    angularVelocity : float
        The initial angular velocity.
    """
    return angularVelocity

def normaliseAngle(angle):
    # Move into pendulum class.
    
    changed = False
    
    while ((greater := angle > np.pi) or 
           (lesser := angle < -np.pi)):
        if greater:
            angle -= 2*np.pi
            print(angle)
        elif lesser:
            angle += 2*np.pi
        
        changed = True
    
    return angle, changed

def simulatePendulum(pendulum,
                     intervalTime = 0.0125,
                     g = 9.81):
    """
    Simulates the motion of a simple pendulum without a damping or driving
    force, uses the Runge Kutta algorithm to solve the differential equation
    for a simple pendulum. Produces x and y coordinates for the motion of the
    pendulum.

    Parameters
    ----------
    pendulum : Pendulum class
        A class representing a point mass attached to a rigid string, the
        pendulum whose motion this function simulates.
    intervalTime : float, optional
        The time bewteen calculations, in seconds.
        The default is 0.0125.
    g : float, optional
        The gravitational acceleration in SI units.
        The default is 9.81.

    Returns
    -------
    positions : list
        List of lists, the list at index 0 contains the x coordinates of
        the motion of the pendulum, the list at index 1 contains the y
        coordinates.
    """
    # Time between calculations must be small.
    if intervalTime > 0.1:
        raise ValueError("Time between calculations must be "
                         "less than or equal to 0.1 seconds, it was "
                         f"instead {intervalTime} seconds.")

    positions = [[], []]
    pendulum.angle, changed = normaliseAngle(pendulum.angle)
    initialAngle = np.copy(pendulum.angle)
    initialAngularVelocity = np.copy(pendulum.angularVelocity)

    loop = False
    approaching = False
    newDistance = 0
    passedMax = 0
    passedPi = 0
    while not loop:
        oldAngle = np.copy(pendulum.angle)
        oldAngularVelocity = np.copy(pendulum.angularVelocity)

        x = pendulum.length * np.sin(pendulum.angle)
        y = -pendulum.length * np.cos(pendulum.angle)
        # Negative ensures that gravity visually appears to act down when
        # plotted.

        positions[0].append(x)
        positions[1].append(y)

        pendulum.angle, pendulum.angularVelocity = RungeKutta(
            dESimplePendulumAngularVelocity, dESimplePendulumAngle,
            intervalTime, pendulum.angle, pendulum.angularVelocity,
            [g, pendulum.length])

        # Keeps angles within less than or equal to pi and greater than or
        # equal to -pi. Used to determine when to stop the simulation, because
        # for certain situations the angle will continually increase, this
        # stops that.
        pendulum.angle, changed = normaliseAngle(pendulum.angle)
        if changed and np.abs(initialAngle) == np.pi:
            passedPi += 1

        # Determines when one full period has been completed, and stops 
        # making new frames once this occurs.
        oldDistance = np.copy(newDistance)
        if initialAngularVelocity == 0 or passedMax == 2:
            newDistance = np.abs(pendulum.angle - initialAngle)
            if ((initialAngle == 0 or np.abs(initialAngle) == np.pi) and 
                passedMax != 2):
                loop = True
            elif newDistance < oldDistance:
                approaching = True
            else:
                if approaching:
                    loop = True
                approaching = False
        elif ((oldAngularVelocity >= 0 and pendulum.angularVelocity < 0) or
              (oldAngularVelocity <= 0 and pendulum.angularVelocity > 0)):
            passedMax += 1
        elif passedPi > 1 and np.abs(initialAngle) == np.pi:
            loop = True
        elif (((oldAngle <= initialAngle and pendulum.angle > initialAngle) or
              (oldAngle >= initialAngle and pendulum.angle < initialAngle)) 
              and np.abs(initialAngle) != np.pi):
            if passedPi > 1:    
                loop = True
            else:
                passedPi += 1
        else:
            # Safeguard if other statements fail.
            if len(positions[0]) == 2000:
                loop = True

    return positions


def produceAnimation(pendulum, positions, frames = 80*10, interval = 12.5):
    """
    Creates an animation from the x and y coordinates produced by the
    simulatePendulum function. The animation will appear with both a mass and
    a string depicted, with a x and y axis.

    Parameters
    ----------
    pendulum : Pendulum class
        A class representing a point mass attached to a rigid string, the
        pendulum whose motion is shown in the animation.
    positions : list
        List of lists, the list at index 0 contains the x coordinates of
        the motion of the pendulum, the list at index 1 contains the y
        coordinates.
    interval : float, optional
        The time bewteen frames, in milliseconds.
        The default is 0.0125.

    Returns
    -------
    ani : matplotlib.animation.TimedAnimation
        The animation depicting the motion of the pendulum.
    """
    fig, ax = plt.subplots(figsize = (5, 5))
    # Specifiying figsize ensures that plot is square when opened in Spyder
    # IDE.

    m = pendulum.length + 0.2*pendulum.length
    # Used to apply limits to the plots used in the animation, so that the
    # pendulum is fully within the plot.

    def update(frame):
        ax.clear()
        # Removes previous positions of the pendulum from the animation.

        ax.scatter(positions[0][frame], positions[1][frame],
                   color = 'black', zorder = 2)
        ax.plot([positions[0][frame], pendulum.pendCoor[0]],
                [positions[1][frame], pendulum.pendCoor[1]],
                color = 'brown', linestyle = '-', zorder = 1)
        # zorder ensures that the mass appears on top of the string, it would
        # look weird otherwise.

        plt.xlim(-m, m)
        plt.ylim(-m, m)

    ani = animation.FuncAnimation(fig = fig, func = update,
                                  frames = len(positions[0]), interval = interval)
    plt.show()
    # Makes sure that the animation appears when using Spyder IDE. Not
    # necessary if the animation is being saved to a file.

    mpl.rcParams['animation.ffmpeg_path'] = (r'E:\\Programs\\ffmpeg'
                                             '\\bin\\ffmpeg.exe')
    #ani.save("file2.mp4")

    return ani
