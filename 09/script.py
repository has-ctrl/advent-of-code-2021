import numpy as np

np_data = np.array([[int(n) for n in row] for row in np.loadtxt("data.txt", dtype=str)])

MIN_X, MIN_Y = 0, 0
MAX_X, MAX_Y = np_data.shape[0] - 1, np_data.shape[1] - 1


def is_lowest(data: np.ndarray, row: int, col: int) -> bool:
    """
    Returns whether a specific coordinate is a local minima (local point).
    """

    def lower_than_up(r: int, c: int) -> bool:
        """
        Returns whether current position is lower than the position up.
        """
        if r == MIN_Y:
            return True
        else:
            return data[r][c] < data[r - 1][c]

    def lower_than_down(r: int, c: int) -> bool:
        """
        Returns whether current position is lower than the position down below.
        """
        if r == MAX_Y:
            return True
        else:
            return data[r][c] < data[r + 1][c]

    def lower_than_left(r: int, c: int) -> bool:
        """
        Returns whether current position is lower than the position to the left.
        """
        if c == MIN_X:
            return True
        else:
            return data[r][c] < data[r][c - 1]

    def lower_than_right(r: int, c: int) -> bool:
        """
        Returns whether current position is lower than the position to the right.
        """
        if c == MAX_X:
            return True
        else:
            return data[r][c] < data[r][c + 1]

    return lower_than_up(row, col) and lower_than_down(row, col) and \
           lower_than_left(row, col) and lower_than_right(row, col)


def find_low_points(data: np.ndarray) -> list:
    """
    Find all of the low points on your heightmap.
    """
    low_points = []
    for row in range(MAX_Y + 1):
        for col in range(MAX_X + 1):
            if is_lowest(data, row, col):
                low_points.append((row, col))

    return low_points


def one(data: np.ndarray) -> int:
    """
    Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your
    heightmap?
    """
    risk_level = 0
    for row, col in find_low_points(data):
        risk_level += 1 + data[row][col]

    return risk_level


def n_basin_neighbours(data: np.ndarray, row: int, col: int) -> int:
    """
    Retrieves all neighbours for coordinate (row, col) that are part of the basin.
    """
    max_height = 9

    def recursive_search(coord_list: list) -> list:
        """
        Recursively search the coordinates list.
        """
        neighbours = coord_list
        n_neighbours = len(neighbours)

        for r, c in neighbours:
            # Basin above is part of the basin.
            if r != MIN_Y and data[r - 1][c] != max_height and (r - 1, c) not in neighbours:
                neighbours.append((r - 1, c))
            # Basin below is part of the basin.
            if r != MAX_Y and data[r + 1][c] != max_height and (r + 1, c) not in neighbours:
                neighbours.append((r + 1, c))
            # Basin left is part of the basin.
            if c != MIN_X and data[r][c - 1] != max_height and (r, c - 1) not in neighbours:
                neighbours.append((r, c - 1))
            # Basin right is part of the basin.
            if c != MAX_X and data[r][c + 1] != max_height and (r, c + 1) not in neighbours:
                neighbours.append((r, c + 1))

        # If no new additions, stop recursive function.
        if n_neighbours == len(neighbours):
            return neighbours
        return recursive_search(neighbours)

    return len(recursive_search([(row, col)]))


def two(data: np.ndarray) -> int:
    """
    Find the three largest basins and multiply their sizes together.
    """
    basin_sizes = []
    for row, col in find_low_points(data):
        basin_sizes.append(n_basin_neighbours(data, row, col))

    n1, n2, n3 = sorted(basin_sizes, reverse=True)[:3]
    return n1 * n2 * n3


print(f"1. {one(np_data)}")
print(f"2. {two(np_data)}")
