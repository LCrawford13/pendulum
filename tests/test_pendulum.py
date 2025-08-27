import pytest
import numpy as np
from Pendulum import Pendulum


def normaliseAngleTest():
    tests = []

    # Test an angle in each quadrant, within -pi to pi.
    tests.append([Pendulum(angle = np.pi / 3), np.pi / 3])
    tests.append([Pendulum(angle = 2 * np.pi / 3), 2 * np.pi / 3])
    tests.append([Pendulum(angle = -np.pi / 4), -np.pi / 4])
    tests.append([Pendulum(angle = -3 * np.pi / 4), -3 * np.pi / 4])

    # Test boundaries of range.
    tests.append([Pendulum(angle = -np.pi), -np.pi])
    tests.append([Pendulum(angle = np.pi), np.pi])

    # Test an angle in each quadrant outside range.
    tests.append([Pendulum(angle = 7 * np.pi / 3), np.pi / 3])
    tests.append([Pendulum(angle = 20 * np.pi / 3), 2 * np.pi / 3])
    tests.append([Pendulum(angle = -21 * np.pi / 5), -np.pi / 5])
    tests.append([Pendulum(angle = -24 * np.pi / 5), -4 * np.pi / 5])

    for test in tests:
        assert test[0].angle == test[1]
