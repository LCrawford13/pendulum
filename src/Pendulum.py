import numpy as np


class Pendulum:
    """
    A class representing a point mass on a rigid string, a pendulum.
    Contains all information required to simulate one, all units are SI.
    All numbers are numpy float64.

    Parameters
    ----------
    length : numpy float64, optional
        Length of pendulum string, should be positive.
        The default is 10.
    angle : numpy float64, optional
        Angle of pendulum, where straight down is zero, left is -pi/2, right
        is pi/2, in radians.
        The default is -pi/2.
    angularVelocity : numpy float64, optional
        Angular velocity of pendulum mass.
        The default is 0.
    pendCoor : numpy ndarray of numpy float64, optional
        The coordinates where the string originates from.
        The default is np.array([0, 0], dtype = 'float64').
    """

    def __init__(
            self,
            length = 1,
            angle = -np.pi / 2,
            angularVelocity = 0,
            pendCoor = np.array([0, 0], dtype = 'float64')):

        if np.float64(length) <= 0:
            raise ValueError("The length of a pendulum must be greater than"
                             " zero.")

        self.length = self.convertFloat(length)
        self.angle = self.convertFloat(angle)
        self.angularVelocity = self.convertFloat(angularVelocity)
        self.pendCoor = self.convertArray(pendCoor)

        self.normaliseAngle()

    def __str__(self):
        return (f"Pendulum Length: {self.length}, "
                f"Pendulum Angle: {self.angle}, "
                f"Pendulum Angular Velocity: {self.angularVelocity}, "
                f"Pendulum Coordinates: {self.pendCoor}.")

    def normaliseAngle(self):
        """
        Checks self.angle to see if it is within -pi (exclusive) to
        pi (inclusive), if it isn't it'll add or subtract two pi until it is.
        """
        while ((greater := self.angle > np.pi) or
               (lesser := self.angle <= -np.pi)):
            if greater:
                self.angle -= 2 * np.pi
            elif lesser:
                self.angle += 2 * np.pi

    @staticmethod
    def convertFloat(fl):
        """
        Checks if the parameter fl is capabale of being converted into
        a numpy float64, while not being an array.

        Parameters
        ----------
        ar: any
            The variable being tested could have any data type,
            it should be an numpy float64, while not being an array.
        """
        if isinstance(fl, (np.ndarray, list)):
            raise ValueError("Parameter must not be an array.")

        return np.float64(fl)

    @staticmethod
    def convertArray(ar):
        """
        Checks if the parameter ar is capabale of being converted into
        a 1D float64 numpy array of length 2. If so, it will be converted
        into such. Some checks are left to the np.float64 function.

        Parameters
        ----------
        ar: any
            The variable being tested could have any data type,
            it should be an ndarray with dtype float64, and length 2.
        """
        if isinstance(ar, (np.ndarray, list)):
            if len(ar) != 2:
                raise ValueError("Parameter must be of length 2, but it "
                                 f"has length {len(ar)}.")

            ar = np.float64(ar)

            if ar.ndim != 1:
                raise ValueError("Parameter must be a 1D array, but it's "
                                 f"{ar.ndim}")
        else:
            raise ValueError("Parameter must be a list or numpy array,"
                             f" but it's {type(ar)}.")

        return ar
