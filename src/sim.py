from Pendulum import Pendulum

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


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

    b1 = func1(consts, oldState1 + a2 * h / 2)
    b2 = func2(consts, oldState2 + a1 * h / 2)

    c1 = func1(consts, oldState1 + b2 * h / 2)
    c2 = func2(consts, oldState2 + b1 * h / 2)

    d1 = func1(consts, oldState1 + c2 * h)
    d2 = func2(consts, oldState2 + c1 * h)

    newState1 = oldState1 + (a2 + 2 * b2 + 2 * c2 + d2) * h / 6
    newState2 = oldState2 + (a1 + 2 * b1 + 2 * c1 + d1) * h / 6

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
    return -np.sin(angle) * consts[0] / consts[1]


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


def simulatePendulum(pendulum,
                     intervalTime = 0.0125,
                     g = -9.81,
                     maxFrames = 2000):
    """
    Simulates the motion of a simple pendulum without a damping or driving
    force, uses the Runge Kutta algorithm to solve the differential equation
    for a simple pendulum. Produces x and y coordinates for the motion of the
    pendulum. It will attempt to return one period of motion.

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
        The default is -9.81.
    maxFrames : int, optional
        The maximum number of frames to simulate, only used in backup for when
        the period can't be determined.
        The default is 2000.

    Returns
    -------
    positions : list
        List of lists, the list at index 0 contains the x coordinates of
        the motion of the pendulum, the list at index 1 contains the y
        coordinates.
    """
    if not isinstance(pendulum, Pendulum):
        raise ValueError("pendulum parameter must be a Pendulum object. Yet "
                         f"it is {type(pendulum)}")
    # Time between calculations must be small.
    if intervalTime > 0.1:
        raise ValueError("Time between calculations must be "
                         "less than or equal to 0.1 seconds, it was "
                         f"instead {intervalTime} seconds.")
    else:
        intervalTime = np.float64(intervalTime)
    # maxFrames must be positive.
    if maxFrames <= 0:
        raise ValueError("Maximum number of frames must be greater than or "
                         f"equal to zero, yet it's {maxFrames}.")
    else:
        maxFrames = np.int64(maxFrames)
    g = np.float64(g)

    positions = []
    pendulum.normaliseAngle()
    initialAngle = np.copy(pendulum.angle)
    initialAngularVelocity = np.copy(pendulum.angularVelocity)

    loop = False

    passedMax = 0
    passedInit = 0
    while not loop:
        oldAngle = np.copy(pendulum.angle)
        oldAngularVelocity = np.copy(pendulum.angularVelocity)

        x = pendulum.length * np.sin(pendulum.angle) + pendulum.pendCoor[0]
        y = pendulum.length * np.cos(pendulum.angle) + pendulum.pendCoor[1]

        positions.append([np.float64(x), np.float64(y)])

        pendulum.angle, pendulum.angularVelocity = RungeKutta(
            dESimplePendulumAngularVelocity, dESimplePendulumAngle,
            intervalTime, pendulum.angle, pendulum.angularVelocity,
            [g, pendulum.length])

        # Keeps angles within less than or equal to pi and greater than -pi.
        # Used to determine when to stop the simulation, because
        # for certain situations the angle will indefinitely increase, this
        # stops that.
        tempAngle = np.copy(pendulum.angle)
        pendulum.normaliseAngle()

        if ((oldAngularVelocity >= 0 and pendulum.angularVelocity < 0) or
           (oldAngularVelocity <= 0 and pendulum.angularVelocity > 0)):
            passedMax += 1

        # Determines when one full period has been completed, and stops
        # making new frames once this occurs.
        if len(positions[0]) == maxFrames:
            # Safeguard if other statements fail.
            loop = True
        elif initialAngularVelocity == 0:
            if (passedMax >= 3 or initialAngle == 0
               or np.abs(initialAngle) == np.pi or g == 0):
                # In the last three cases, the pendulum won't move.
                loop = True
        elif initialAngularVelocity != 0:
            if len(positions[0]) != 1 and tempAngle != pendulum.angle:
                if np.abs(initialAngle) != np.pi:
                    # Passing pi triggers the if statement below,
                    # this compensates.
                    passedInit -= 1
                else:
                    # The if statement below never triggers if the inital angle
                    # is pi, this compenstates.
                    passedInit += 1

            if ((oldAngle < initialAngle and pendulum.angle > initialAngle) or
               (oldAngle > initialAngle and pendulum.angle < initialAngle)):
                passedInit += 1

            if ((passedMax == 0 and passedInit >= 1) or
               (passedMax >= 1 and passedInit >= 2)):
                # First case is for a pendulum completing full circles, second
                # case is for pendulum swinging back and forth.
                loop = True

    return np.float64(positions)


def produceAnimation(pendulum, positions, interval = 12.5,
                     fig = None, ax = None):
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
        The default is 12.5, so 80fps.

    Returns
    -------
    ani : matplotlib.animation.TimedAnimation
        The animation depicting the motion of the pendulum.
    """
    if fig is None or ax is None:
        # Specifiying figsize ensures that plot is square when opened in Spyder
        # IDE.
        fig, ax = plt.subplots(figsize = (5, 5), dpi = 150)

    pendX = pendulum.pendCoor[0]
    pendY = pendulum.pendCoor[1]
    # Used to apply limits to the plots used in the animation, so that the
    # pendulum is fully within the plot.
    m = pendulum.length + 0.2 * pendulum.length

    # zorder ensures that the mass appears on top of the string, it would
    # look weird otherwise.
    mass = ax.scatter([], [], color = 'black', zorder = 2)
    string = ax.plot([], [], color = 'brown', linestyle = '-', zorder = 1)[0]

    ax.set(xlim = [-m + pendX, m + pendX], ylim = [-m + pendY, m + pendY])

    def update(frame):
        x = positions[frame][0]
        y = positions[frame][1]

        mass.set_offsets([x, y])
        string.set_xdata([x, pendX])
        string.set_ydata([y, pendY])

        return (mass, string, )

    ani = animation.FuncAnimation(fig = fig, func = update,
                                  frames = len(positions),
                                  interval = interval, blit = True)

    # Makes sure that the animation appears.
    return ani
