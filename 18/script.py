import math
from itertools import permutations


def one(data: list[list[int]]) -> int:
    """
    Add up all of the snailfish numbers from the homework assignment in the order they appear. What is the magnitude of
    the final sum?
    """
    sn = data[0]
    for next_sn in data[1:]:
        sn = add(sn, next_sn)

        # Only break if it cannot be further reduced.
        while True:
            if must_explode(sn):
                sn = explode(sn)
            elif must_split(sn):
                sn = split(sn)
            else:
                break

    return magnitude(sn)


def two(data: list[list[int]]) -> int:
    """
    What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment?
    """
    perm_data = permutations(data, r=2)
    return max([one([x, y]) for x, y in perm_data])


def add(a: list, b: list) -> list[list, list]:
    """
    Adds two snailnumbers (a and b).
    """
    return [[n, depth + 1] for n, depth in a + b]


def must_explode(li: list) -> bool:
    """
    Returns whether the current snailnumber must explode (nested list of 4).
    """
    return max([d1 for (_, d1), (_, d2) in zip(li, li[1:]) if d1 == d2]) >= 5


def explode(li: list) -> list:
    """
    Leftmost of any pair that is nested inside four pairs explodes.
    """
    res = li
    for i, ((n1, depth1), (n2, depth2)) in enumerate(zip(li, li[1:])):
        if depth1 >= 5 and depth1 == depth2:
            # If left number exists.
            if i > 0:
                res[i-1][0] += n1
            # If right number exists.
            if i < len(li) - 2:
                res[i+2][0] += n2
            # Replace exploding pair by zero.
            res = res[:i] + [[0, depth1 - 1]] + res[i+2:]
            break

    return res


def must_split(li: list) -> bool:
    """
    Returns whether the current snailnumber must split (number higher than 10).
    """
    return max([n for n, _ in li]) >= 10


def split(li: list) -> list:
    """
    Replace regular number by a pair (left round down, right round up).
    """
    res = li
    for i, (n, depth) in enumerate(li):
        if n >= 10:
            left = [math.floor(n/2), depth + 1]
            right = [math.ceil(n/2), depth + 1]
            # Replace number-that-was-split by a pair.
            res = res[:i] + [left, right] + res[i+1:]
            break

    return res


def magnitude(li: list) -> int:
    """
    Iteratively calculates the magnitude of the reduced snailnumber.
    """
    temp = li
    while len(temp) > 1:
        for i, ((n1, depth1), (n2, depth2)) in enumerate(zip(temp, temp[1:])):
            if depth1 == depth2:
                # Replace nested pair with magnitude.
                mag = n1 * 3 + n2 * 2
                temp = temp[:i] + [[mag, depth1 - 1]] + temp[i+2:]
                break

    return temp[0][0]


def transform_input(data: list[str]) -> list[list]:
    """
    Transforms each snailnumber to a flat list of the number and the depth.
    """
    res = []
    for li in data:
        sn, depth = [], 0
        # Loop through each character ([, ], or int).
        for c in li:
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
            elif c.isdigit():
                sn.append([int(c), depth])
        res.append(sn)

    return res


with open("data.txt", "r") as f:
    input_data = transform_input(f.read().split("\n"))


print(f"1. {one(input_data)}")
print(f"2. {two(input_data)}")
