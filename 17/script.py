import re
from collections import defaultdict


def one(data: list) -> int:
    """
    Find the initial velocity that causes the probe to reach the highest y position and still eventually be within the
    target area after any step. What is the highest y position it reaches on this trajectory?
    """
    def find_highest_y(y: int) -> int:
        """
        """
        res = y
        for y_step in range(y):
            res += y_step
        return res

    def find_largest_y_direction() -> int:
        """
        Find the y direction where the largest y comes between the y_min and y_max.
        """
        if y_min > 0:  # If target is positive, the largest y dir is the max.
            return y_max
        else:  # If negative, the largest y dir is the reverse y +1 (because of additional speed).
            return abs(y_min+1)

    _, _, y_min, y_max = data
    y_dir = find_largest_y_direction()
    return find_highest_y(y_dir)


def two(data: list) -> int:
    """
    How many distinct initial velocity values cause the probe to be within the target area after any step?
    """
    def find_x_directions() -> dict[set[int]]:
        """
        Find the x direction where additive factorial (triangular numbers) res < x_max. These show possible Xs and the
        number of steps it takes to get there.
        """
        res = defaultdict(set)
        # Loop through all possible values for x.
        for i in reversed(range(x_max+1)):
            x = i
            steps = 1
            if x_min <= i <= x_max:
                res[steps].add(i)
            # Loop through smaller additional x-1 steps (triangular numbers).
            for j in reversed(range(i)):
                x += j
                steps += 1
                if x > x_max:
                    break
                elif x_min <= x <= x_max:
                    res[steps].add(i)
                    # If the velocity comes to zero, but it is still within the bounds.
                    next_x = x + sum(range(j))
                    if x_min <= next_x <= x_max:
                        for s in range(abs(y_min+1)*2):
                            res[steps+s].add(i)
        return res

    def find_y_directions() -> dict[set[int]]:
        """
        Find the x direction where additive factorial (triangular numbers) res < x_max. These show possible Xs and the
        number of steps it takes to get there.
        """
        res = defaultdict(set)
        # Loop through all possible values for y.
        y_range = range(y_min, max(abs(y_min)+1, y_max)+1)
        for i in reversed(y_range):
            y = i
            steps = 1
            if y_min <= i <= y_max:
                res[steps].add(i)

            j = y
            # Loop through all drag-adjusted values.
            while j >= y_min:
                y -= 1
                j += y
                steps += 1
                if y_min <= j <= y_max:
                    res[steps].add(i)
        return res

    x_min, x_max, y_min, y_max = data
    x_dirs, y_dirs = find_x_directions(), find_y_directions()

    # Loop through all steps (common keys).
    values = set()
    for k in x_dirs.keys() & y_dirs.keys():
        xs, ys = x_dirs[k], y_dirs[k]
        values.update([(x, y) for x in xs for y in ys])

    return len(values)


with open("data.txt", "r") as f:
    input_data = [int(x) for x in re.findall(r'[+-]?\d+', f.readline())]


print(f"1. {one(input_data)}")
print(f"2. {two(input_data)}")
