import numpy as np
from Pendulum import Pendulum
import pytest


def test_str():
    length = np.float64(5)
    angle = np.float64(np.pi / 3)
    angularVelocity = np.float64(4.3)
    pendCoor = np.array([3, 2], dtype = np.float64)

    p = Pendulum(length, angle, angularVelocity, pendCoor)
    assert str(p) == (f"Pendulum Length: {length}, "
                      f"Pendulum Angle: {angle}, "
                      f"Pendulum Angular Velocity: {angularVelocity}, "
                      f"Pendulum Coordinates: {pendCoor}.")


def test_normaliseAngle():
    def testNormaliseAngle(a1, a2):
        assert np.round(Pendulum(angle = a1).angle, 10) == np.round(a2, 10)

    # Test an angle in each quadrant, within -pi to pi.
    testNormaliseAngle(np.pi / 3, np.pi / 3)
    testNormaliseAngle(2 * np.pi / 3, 2 * np.pi / 3)
    testNormaliseAngle(-np.pi / 4, -np.pi / 4)
    testNormaliseAngle(-3 * np.pi / 4, -3 * np.pi / 4)

    # Test boundaries of range.
    testNormaliseAngle(-np.pi, -np.pi)
    testNormaliseAngle(np.pi, np.pi)

    # Test an angle in each quadrant outside range.
    testNormaliseAngle(7 * np.pi / 3, np.pi / 3)
    testNormaliseAngle(20 * np.pi / 3, 2 * np.pi / 3)
    testNormaliseAngle(-21 * np.pi / 5, -np.pi / 5)
    testNormaliseAngle(-24 * np.pi / 5, -4 * np.pi / 5)


def test_floatInit():
    def testFloatRaise(value):
        with pytest.raises(ValueError):
            Pendulum(length = value)
        with pytest.raises(ValueError):
            Pendulum(angle = value)
        with pytest.raises(ValueError):
            Pendulum(angularVelocity = value)

    # Test an incorrect input as a string.
    testFloatRaise("three")
    # Test an incorrect input as a list.
    testFloatRaise([1, 3])
    # Test an incorrect input as an ndarray.
    testFloatRaise(np.array([4, 3]))
    # Test a length of zero. DOESN'T WORK!!!!!
    with pytest.raises(ValueError):
        Pendulum(length = "0")

    def testFloat(value, result):
        assert Pendulum(length = value).length == result
        assert Pendulum(angle = value).angle == result
        assert Pendulum(angularVelocity = value).angularVelocity == result

    # Test a boolean, True is 1, False is 0.
    testFloat(False, 0)
    testFloat(True, 1)
    # Test a string with an int in it, both positive and negative.
    testFloat("-3", -3)
    testFloat("3", 3)
    # Test a string with a float in it, both positive and negative.
    testFloat("-2.1", -2.1)
    testFloat("2.1", 2.1)
    # Test an int, both positive and negative.
    testFloat(-2, -2)
    testFloat(2, 2)
    # Test a float, both positive and negative.
    testFloat(-1.9, -1.9)
    testFloat(1.9, 1.9)


test_floatInit()
