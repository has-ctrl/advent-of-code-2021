import numpy as np

with open("data.txt") as f:
    np_data = np.array([[x.split(","), y.split(",")] for x, y in [line.split(" -> ") for line in f.read().split("\n")]], dtype=int)


def is_straight(c1: np.ndarray, c2: np.ndarray) -> bool:
    """
    Tests whether the line coordinates are horizontal or vertical (straight). In other words, are the X coordinates
    equal, or the Y coordinates equal.
    """

    return np.equal(c1[0], c2[0]) or np.equal(c1[1], c2[1])


def coordinates_between(c1: np.ndarray, c2: np.ndarray) -> list:
    """
    Returns all coordinates between two points in the line [(x1, y1) -> (x2, y2)].
    """
    x = np.linspace(c1[0], c2[0], num=abs(c1[0] - c2[0])+1)
    y = np.linspace(c1[1], c2[1], num=abs(c1[1] - c2[1])+1)

    if is_straight(c1, c2):
        return [(i, j) for i in x for j in y]
    else:
        return [(i, j) for i, j in zip(x, y)]


def one(data: np.ndarray) -> int:
    """
    Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
    """
    freq = {}

    for line in data:
        c1, c2 = line
        if is_straight(c1, c2):
            coordinates = coordinates_between(c1, c2)
            for c in coordinates:
                if c in freq:
                    freq[c] += 1
                else:
                    freq[c] = 1

    return len([k for k, v in freq.items() if v > 1])


def two(data: np.ndarray) -> int:
    """
    Consider all of the lines. At how many points do at least two lines overlap?
    """

    freq = {}

    for line in data:
        c1, c2 = line
        coordinates = coordinates_between(c1, c2)
        for c in coordinates:
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1

    return len([k for k, v in freq.items() if v > 1])


print(f"1. {one(np_data)}")
print(f"2. {two(np_data)}")
