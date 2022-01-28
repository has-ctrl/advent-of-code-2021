import numpy as np

np_data = np.array([[int(bit) for bit in bit_str] for bit_str in np.loadtxt("data.txt", dtype=str)])


def one(data: np.ndarray, n_steps: int = 100) -> int:
    """
    Given the starting energy levels of the dumbo octopuses in your cavern, simulate 100 steps.
    How many total flashes are there after 100 steps?
    """
    flash_energy = 9
    flash_reset = 0
    flash_count = 0
    prev_state = data.copy()

    def get_adjacents(row: int, col: int) -> list:
        """
        Retrieve all valid adjacents for the (row, col) combination.
        """
        def is_valid(new_r: int, new_c: int) -> bool:
            """
            Returns if a coordinate (new_r, new_c) is a valid one in the grid.
            """
            min_x, min_y = 0, 0
            max_x, max_y = len(data[0]), len(data)
            return min_x <= new_r < max_x and min_y <= new_c < max_y

        return [(row + r, col + c) for r in (-1, 0, 1) for c in (-1, 0, 1) if is_valid(row + r, col + c)]

    def recursive_search(step_state: np.ndarray, coord_list: list, flashed_list: list = None) -> (np.ndarray, int):
        """
        Recursively 'flash', and use the get_adjacents function for every step. Returns the state after the step and
        the flash count.
        """
        if not flashed_list:
            flashed_list = []

        coords = coord_list
        n_flashed = len(flashed_list)

        # Retrieve all adjacents for the non-flashed coordinates.
        adjacents = [
            coord for adjacents_temp in
            [get_adjacents(x, y) for x, y in coords if (x, y) not in flashed_list]
            for coord in adjacents_temp
        ]

        # Keep track of which coordinates have flashed.
        flashed_list.extend(coords)

        # Add one for each of the adjacents.
        for (x, y) in adjacents:
            step_state[y, x] += 1

        # Find new coordinates and add them to coords.
        new_ys, new_xs = np.where(step_state > flash_energy)
        new_coords = [coord for coord in list(zip(new_xs, new_ys)) if coord not in flashed_list]

        # If no new flashes, return state and the flash count, otherwise search further.
        if n_flashed == len(flashed_list):
            return step_state, n_flashed

        return recursive_search(step_state, new_coords, flashed_list)

    for step in range(n_steps):

        # 1. The energy level of each octopus increases by 1.
        state = prev_state + 1

        # 2. If 9 -> flash. If flash -> adjacent +1.
        ys, xs = np.where(state > flash_energy)
        init_coords = list(zip(xs, ys))
        state, count = recursive_search(state, init_coords)
        flash_count += count

        # 3. Set flashed octopuses to zero.
        prev_state = np.where(state > flash_energy, flash_reset, state)

        # For part 2: if all are zero, break the loop and return the step.
        if np.all(prev_state == 0):
            return step + 1

    return flash_count


def two(data: np.ndarray, n_steps: int = 1000) -> int:
    """
    If you can calculate the exact moments when the octopuses will all flash simultaneously, you should be able to
    navigate through the cavern. What is the first step during which all octopuses flash?
    """
    return one(data, n_steps)


print(f"1. {one(np_data)}")
print(f"2. {two(np_data)}")
