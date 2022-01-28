import numpy as np

test_data = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])
np_data = np.loadtxt("data.txt", delimiter=",", dtype=int)


def one(data: np.ndarray) -> int:
    """
    Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they
    spend to align to that position?
    """
    median = np.median(data).astype(int)
    return np.absolute(data - median).sum()


def two(data: np.ndarray) -> int:
    """
    Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an
    escape route! How much fuel must they spend to align to that position?
    """
    mean = np.mean(data).astype(int)
    diff = np.absolute(data - mean)

    # 'Factorial for addition' is the same as (X^2 + X) / 2
    return ((diff * diff + diff) / 2).astype(int).sum()


print(f"1. {one(np_data)}")
print(f"2. {two(np_data)}")
