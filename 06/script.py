import numpy as np


np_data = np.loadtxt("data.txt", delimiter=",", dtype=int)


def one(data: np.ndarray, days: int = 80) -> int:
    """
    Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?
    """
    state = data.copy()
    timer, new_timer = 6, 8

    for day in range(days):

        # Add new lanternfish (8+1) for every zero
        state = np.append(state, np.full(np.count_nonzero(state == 0), new_timer+1))

        # Replace all zeros with 6+1
        state = np.where(state == 0, timer+1, state)

        # Subtract 1 day for all values (e.g. 8+1 -> 8)
        state = state - 1

    return state.size


def two(data: np.ndarray, days: int = 256) -> int:
    """
    How many lanternfish would there be after 256 days?

    (Code needs to be more efficient)
    """
    timer, new_timer = 6, 8
    state = {k: v for (k, v) in zip(*np.unique(data.copy(), return_counts=True))}
    for x in range(new_timer+1):
        state[x] = 0 if x not in state else state[x]

    for day in range(days):
        temp_state = state.copy()

        for t, freq in state.items():
            if t == 0:
                temp_state[timer] += freq
                temp_state[new_timer] += freq
            else:
                temp_state[t - 1] += freq

            temp_state[t] -= freq

        state = temp_state

    return sum(state.values())


print(f"1. {one(np_data)}")
print(f"2. {two(np_data)}")
