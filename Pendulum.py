import numpy as np

class Pendulum:
    def __init__(
            self,
            mass = np.float64(1),
            velocityInitial = np.array([0, -1], dtype = 'float64'),
            pendCoor = np.array([0, 0], dtype = 'float64'),
            massInitialCoor = np.array([-10, 0], dtype = 'float64')
            ):
        #Type Checking for object parameters.
        if isinstance(mass, (float, int)):
            if not isinstance(mass, np.float64):
                mass.astype('float64')
        else:
            raise ValueError("Mass parameter must be int or float, not "\
                             f"{type(mass)}.")
        
        if (velocityInitial.dtype.kind in (np.typecodes["AllFloat"] or 
                                           np.typecodes["AllInteger"])
            ):
            if velocityInitial.dtype != 'float64':
                velocityInitial.astype('float64')
        else:
            raise ValueError("Initial Velocity parameter must be a "\
                             "numpy array, with type of int or float, not "\
                             f"{velocityInitial.dtype}.")
        
        self.mass = mass
        self.velocityInitial = velocityInitial
        self.pendCoor = pendCoor
        self.massInitialCoor = massInitialCoor
            

