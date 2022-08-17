from collections import defaultdict
from heapq import heappop, heappush
import numpy as np
import math


def calculate_lowest_risk(data) -> int:
    """
    Use the A* search algorithm to retrieve the shortest path and associated (lowest) risk (with priority queue).
    """

    def is_valid_node(_x: int, _y: int) -> bool:
        """
        Check whether the proposed node is valid.
        """
        return min_x <= _x <= max_x and min_y <= _y <= max_y

    min_x = min_y = 0
    max_x = max_y = data.shape[0] - 1

    start_node = (min_x, min_y)
    end_node = (max_x, max_y)

    risk_dict = defaultdict(lambda: math.inf)
    risk_dict[start_node] = 0

    open_list = []
    heappush(open_list, (0, start_node))

    unvisited = {(x, y) for x in range(len(data)) for y in range(len(data))}

    # Loop until the end node has been found.
    while end_node in unvisited:
        current_risk, current = heappop(open_list)

        # Double check.
        if current not in unvisited:
            continue

        child_nodes = []
        for x_pos_change, y_pos_change in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # left, right, down, up.

            x, y = current

            # New node positions.
            x_pos = x + x_pos_change
            y_pos = y + y_pos_change

            # Append new node to child nodes if it is valid.
            if is_valid_node(x_pos, y_pos):
                child_nodes.append((x_pos, y_pos))

        for child_node in child_nodes:

            # Only consider child nodes not in closed list.
            if child_node not in unvisited:
                continue

            # Only update (cumulative) risk only if it is lower.
            child_risk = min(
                risk_dict[child_node],
                risk_dict[current] + data[child_node[1]][child_node[0]]
            )

            risk_dict[child_node] = child_risk
            heappush(open_list, (child_risk, child_node))

        unvisited.remove(current)

    return risk_dict[end_node]


def update_map(data) -> np.ndarray:
    """
    Update the risk for a 5x5 map.
    """
    max_x, max_y = data.shape
    risk_map = np.empty((max_x * 5, max_y * 5))

    for y_index, y in enumerate(risk_map):
        for x_index, x in enumerate(y):
            risk = data[y_index % max_y][x_index % max_x]  # The risk value in the regular map (data).

            # Update the risk value (1>2, 2>3, ..., 9>1).
            risk_map[y_index][x_index] = (risk + ((y_index // max_y) + (x_index // max_x)) - 1) % 9 + 1

    return risk_map


def one(data: np.ndarray) -> int:
    """
    What is the lowest total risk of any path from the top left to the bottom right?
    """
    return calculate_lowest_risk(data)


def two(data: np.ndarray) -> int:
    """
    Using the full map, what is the lowest total risk of any path from the top left to the bottom right?
    """
    return int(one(update_map(data)))


np_data = np.array([[int(bit) for bit in bit_str] for bit_str in np.loadtxt("data.txt", dtype=str)])


print(f"1. {one(np_data)}")
print(f"2. {two(np_data)}")


