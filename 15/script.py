import numpy as np
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    """
    Default Node in the graph.
    """
    x_position: int
    y_position: int
    parent: Any  # Node datatype
    g: int = 0
    h: int = 0
    f: int = 0

    def __lt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return self.x_position == other.x_position and self.y_position == other.y_position


def calculate_lowest_risk(data) -> int:
    """
    Use the A* search algorithm to retrieve the shortest path and associated (lowest) risk.
    """

    def is_valid_node(n: Node) -> bool:
        """
        Check whether the proposed node is valid.
        """
        return min_x <= n.x_position <= max_x and min_y <= n.y_position <= max_y

    min_x = min_y = 0
    max_x = max_y = data.shape[0] - 1

    start_node = Node(min_x, min_y, None)
    end_node = Node(max_x, max_y, None)

    open_list = [start_node]
    closed_list = []

    # Loop until the end node has been found.
    while open_list:

        # Get the current node (lowest f score)
        open_list.sort(reverse=True)
        current_node = open_list[0]
        current_index = 0

        # Remove current node from open list and add to closed list.
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the end node.
        if current_node == end_node:
            return current_node.g  # reconstruct_path(current_node)

        # Generate potential paths (children nodes).
        child_nodes = []
        for x_pos_change, y_pos_change in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # left, right, down, up.

            # New node positions.
            x_pos = current_node.x_position + x_pos_change
            y_pos = current_node.y_position + y_pos_change

            # Append new node to child nodes if it is valid.
            new_node = Node(x_pos, y_pos, current_node)
            if is_valid_node(new_node):
                child_nodes.append(new_node)

        # Loop through child nodes.
        for child_node in child_nodes:

            to_consider: bool = True

            # Only consider child nodes not in closed list.
            if child_node in closed_list:
                continue

            child_node.g = current_node.g + data[current_node.y_position][current_node.x_position]
            child_node.h = abs(child_node.x_position - end_node.x_position) + \
                           abs(child_node.y_position - end_node.y_position)
            child_node.f = child_node.g + child_node.h

            # Only consider child nodes for which the cost (g) is lower.
            if child_node in open_list:
                for open_node in open_list:
                    if child_node == open_node and child_node.g > open_node.g:
                        to_consider = False
                        break

            if to_consider:
                open_list.append(child_node)


np_data = np.array([[int(bit) for bit in bit_str] for bit_str in np.loadtxt("data.txt", dtype=str)])


def one(data: np.ndarray) -> int:
    """
    What is the lowest total risk of any path from the top left to the bottom right?
    """
    return calculate_lowest_risk(data)


print(f"1. {one(np_data)}")
