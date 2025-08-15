import numpy as np

class Pendulum:
    """
    A class representing one mass on a string, a pendulum. Contains all 
    information required to simulate one, all units are SI. All numbers are
    numpy float64.

    Parameters
    ----------
    mass : numpy float64
        Mass of mass attached to pendulum string. 
        The default is 1.
    length : numpy float64
        Length of pendulum string. 
        The default is 10.
    pendCoor : numpy ndarray of numpy float64
        The coordinates where the string originates from. 
        The default is np.array([0, 0], dtype = 'float64').
    massCoor : numpy ndarray of numpy float64
        The coordinates of the mass on string. 
        The default is np.array([-10, 0], dtype = 'float64').
    """
    def __init__(
            self,
            mass = 1,
            length = None,
            pendCoor = np.array([0, 0], dtype = 'float64'),
            massCoor = None
            ):
        self.mass = np.abs(self.convertFloat(mass))
        self.pendCoor = self.convertArray(pendCoor)
        
        #Allows pendulum length and the initial mass coordinates to be 
        #dynamically determined depending on whether the user specified 
        #the values for the two variables.
        lengthBool = (length is None)
        massCoorBool = (massCoor is None)
        if massCoorBool and lengthBool:
            self.length = np.float64(10)
            self.massCoor = np.array([-10 + self.pendCoor[0], 
                                     self.pendCoor[1]],
                                     dtype = 'float64')
        elif massCoorBool and not lengthBool:
            self.length = np.abs(self.convertFloat(length))
            self.massCoor = np.array([-self.length + self.pendCoor[0],
                                     self.pendCoor[1]],
                                     dtype = 'float64')
        elif not massCoorBool and lengthBool:
            self.massCoor = self.convertArray(massCoor)
            self.length = np.abs(np.float64(np.linalg.norm(
                                self.pendCoor - self.massCoor)))
        else:
            self.massCoor = self.convertArray(massCoor)
            self.length = np.abs(self.convertFloat(length))
            
            calcLength = np.linalg.norm(self.pendCoor - self.massCoor)
            if calcLength != self.length:
                raise ValueError("Specified length of pendulum "\
                                 f"({self.pendLength}) doesn't match "\
                                 f"calculated length ({calcLength}).")
            
    def __str__(self):
        return (f"Mass: {self.mass}, Pendulum Length: {self.length}, "\
                f"Mass Coordinates: {self.massCoor}, "\
                f"Pendulum Coordinates: {self.pendCoor}, ")

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
                raise ValueError("Parameter must be of length 2, but it "\
                                 f"has length {len(ar)}.")
            
            ar = np.float64(ar)
            
            if ar.ndim != 1:
                raise ValueError("Parameter must be a 1D array, but it's "\
                                 f"{ar.ndim}")
        else:
            raise ValueError("Parameter must be a list or numpy array,"\
                             f" but it's {type(ar)}.")

        return ar