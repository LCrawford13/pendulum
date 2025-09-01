import numpy as np
import numpy.testing as nt
from Pendulum import Pendulum


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
        nt.assert_allclose(Pendulum(angle = a1).angle, a2, 1e-10)

    # Test an angle in each quadrant, within -pi to pi.
    testNormaliseAngle(np.pi / 3, np.pi / 3)
    testNormaliseAngle(2 * np.pi / 3, 2 * np.pi / 3)
    testNormaliseAngle(-np.pi / 4, -np.pi / 4)
    testNormaliseAngle(-3 * np.pi / 4, -3 * np.pi / 4)

    # Test boundaries of range.
    testNormaliseAngle(-np.pi, np.pi)
    testNormaliseAngle(np.pi, np.pi)

    # Test an angle in each quadrant outside range.
    testNormaliseAngle(7 * np.pi / 3, np.pi / 3)
    testNormaliseAngle(20 * np.pi / 3, 2 * np.pi / 3)
    testNormaliseAngle(-21 * np.pi / 5, -np.pi / 5)
    testNormaliseAngle(-24 * np.pi / 5, -4 * np.pi / 5)


def test_floatInit():
    def testFloatRaise(value):
        nt.assert_raises(ValueError, Pendulum, length = value)
        nt.assert_raises(ValueError, Pendulum, angle = value)
        nt.assert_raises(ValueError, Pendulum, angularVelocity = value)

    # Test an incorrect input as a string.
    testFloatRaise("three")
    # Test an incorrect input as a list.
    testFloatRaise([1, 3])
    # Test an incorrect input as an ndarray.
    testFloatRaise(np.array([4, 3]))
    # Test a length of zero and less.
    nt.assert_raises(ValueError, Pendulum, length = 0)
    nt.assert_raises(ValueError, Pendulum, length = -6)

    def testFloat(value, result, neg = False):
        if not neg:
            assert Pendulum(length = value).length == result
        assert Pendulum(angle = value).angle == result
        assert Pendulum(angularVelocity = value).angularVelocity == result

    # Test a boolean, True is 1, False is 0.
    testFloat(False, 0, True)
    testFloat(True, 1)
    # Test a string with an int in it, both positive and negative.
    testFloat("-3", -3, True)
    testFloat("3", 3)
    # Test a string with a float in it, both positive and negative.
    testFloat("-2.1", -2.1, True)
    testFloat("2.1", 2.1)
    # Test an int, both positive and negative.
    testFloat(-2, -2, True)
    testFloat(2, 2)
    # Test a float, both positive and negative.
    testFloat(-1.9, -1.9, True)
    testFloat(1.9, 1.9)


def test_arrayInit():
    def testList(value):
        nt.assert_raises(ValueError, Pendulum, pendCoor = value)

    # Test a string.
    testList("List")
    # Test an integer.
    testList(5)
    # Test a float.
    testList(4.3)
    # Test a boolean.
    testList(True)
    # Test a list of length not equal to two.
    testList([1, 2, 3])
    # Test a list of dimension not equal to one.
    testList([[2, 3]])
    # Test a list of strings.
    testList(["three", "four"])
    # Test an ndarray of length not equal to one.
    testList(np.array([1, 2, 3, 4]))
    # Test an ndarray of dimension not equal to one.
    testList(np.array([[1, 2], [2, 4]]))
    # Test an ndarray of strings.
    testList(np.array(["one", "two"]))

    def assertList(value, result):
        nt.assert_equal(Pendulum(pendCoor = value).pendCoor, result)

    # Test a list/ndarray of integers.
    array1 = np.array([2, 3], dtype = 'float64')
    assertList([2, 3], array1)
    assertList(array1, array1)
    # Test a list/ndarray of floats.
    array2 = np.array([-2.2, 3.5], dtype = 'float64')
    assertList([-2.2, 3.5], array2)
    assertList(array2, array2)
    # Test a list/ndarray of integers and floats.
    array3 = np.array([2.8, 3], dtype = 'float64')
    assertList([2.8, 3], array3)
    assertList(array3, array3)
    # Test a list/ndarray of strings with numbers in.
    array4 = np.array([2, -3.4], dtype = 'float64')
    assertList(["2", "-3.4"], array4)
    assertList(np.array(["2", "-3.4"]), array4)
    # Test a list/ndarray of booleans.
    array5 = np.array([1, 0], dtype = 'float64')
    assertList([True, False], array5)
    assertList(np.array([True, False]), array5)
