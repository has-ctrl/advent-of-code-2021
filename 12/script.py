import numpy as np

START_NODE, END_NODE = "start", "end"


def load_data(file_path: str) -> dict:
    """
    Converts the .txt data to dict with the start_node as key and a list of end_nodes as value.
    """
    temp_data = [tuple(edge.split("-")) for edge in np.loadtxt(file_path, dtype=str)]
    temp_data += [tuple(reversed(edge)) for edge in temp_data]

    data = {}
    for start_node, end_node in temp_data:
        # Exclude end node from linking to anywhere.
        if start_node != END_NODE:
            data[start_node] = data.get(start_node, []) + [end_node]
    return data


def find_all_paths(graph: dict, start_node: str, current_path: list = None, double_visit: bool = False):
    """
    Find all possible and valid paths through the graph {data}.
    """

    def is_valid(name: str) -> bool:
        """
        Returns whether a node can be visited (i.e. avoids a small cave if it has been already visited once for one() or
        twice for two().
        """
        if double_visit and node != START_NODE:
            seen = set()
            duplicate_cave_list = [x for x in current_path if (x in seen or seen.add(x)) and x.islower()]
            # If there is a maximum of one duplicate small cave in the current path, return True.
            return len(duplicate_cave_list) <= 1
        else:
            return not (name.islower() and name in current_path)

    if not current_path:
        current_path = []

    current_path = current_path + [start_node]

    # If we have reached the end node (for a singular path), return the path.
    if start_node == END_NODE:
        return [current_path]

    all_paths = []
    for node in graph[start_node]:
        # Avoid small caves that have already been traversed (or a single small cave at most twice).
        if is_valid(node):
            paths = find_all_paths(graph, node, current_path, double_visit=double_visit)
            for path in paths:
                all_paths.append(path)

    return all_paths


def one(data: dict) -> int:
    """
    How many paths through this cave system are there that visit small caves at most once?
    """
    return len(find_all_paths(data, START_NODE))


def two(data: dict) -> int:
    """
    Given you can visit a small cave twice, how many paths through this cave system are there?
    """
    return len(find_all_paths(data, START_NODE, double_visit=True))


dict_data = load_data("data.txt")

print(f"1. {one(dict_data)}")
print(f"2. {two(dict_data)}")
