import numpy as np

direction_data = np.loadtxt("data.txt", dtype=str, usecols=[0])
unit_data = np.loadtxt("data.txt", dtype=int, usecols=[1])


def one(directions: np.ndarray, units: np.ndarray) -> int:
    """
    Calculate the horizontal position and depth you would have after following the planned course.
    What do you get if you multiply your final horizontal position by your final depth?
    """
    h_pos = 0
    v_pos = 0

    for d, u in zip(directions, units):
        if d == "forward":
            h_pos += u
        elif d == "down":
            v_pos += u
        elif d == "up":
            v_pos -= u
        else:
            raise ValueError(f"Incorrect direction '{d}' passed.")

    return h_pos * v_pos


def two(directions: np.ndarray, units: np.ndarray) -> int:
    """
    Using this new interpretation of the commands, calculate the horizontal position and depth you would have after
    following the planned course. What do you get if you multiply your final horizontal position by your final depth?
    """
    h_pos = 0
    v_pos = 0
    aim = 0

    for d, u in zip(directions, units):
        if d == "forward":
            h_pos += u
            v_pos += u * aim
        elif d == "down":
            aim += u
        elif d == "up":
            aim -= u
        else:
            raise ValueError(f"Incorrect direction '{d}' passed.")

    return h_pos * v_pos


print(f"1. {one(direction_data, unit_data)}")
print(f"2. {two(direction_data, unit_data)}")
