import numpy as np

np_data = np.loadtxt("data.txt")


def one(data: np.ndarray) -> int:
    """
    To do this, count the number of times a depth measurement increases from the previous measurement.
    (There is no measurement before the first measurement.)
    """
    prev = np.nan
    count = 0
    for i in data:
        if not np.isnan(prev):
            if prev < i:
                count += 1
        prev = i
    return count


def two(data: np.ndarray) -> int:
    """
    Your goal now is to count the number of times the sum of measurements in this sliding window increases from the
    previous sum. So, compare A with B, then compare B with C, then C with D, and so on. Stop when there aren't enough
    measurements left to create a new three-measurement sum.
    """
    return one(np.convolve(data, np.ones(3, dtype=int), mode="valid"))


print(f"1. {one(np_data)}")
print(f"2. {two(np_data)}")
