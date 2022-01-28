import numpy as np


with open("data.txt") as f:
    draws = np.array([int(d) for d in f.readline().split(",")])
    boards = np.array([[[int(n) for n in r.split()] for r in b.split("\n")] for b in f.read()[1:].split("\n\n")])


def bingo(data: np.ndarray, fill: int):
    """
    Returns horizontal (rows) and vertical (columns) bingo. TRUE if bingo. FALSE if not.
    """
    transposed_data = np.transpose(data)

    return any(np.equal(data, [fill for _ in range(5)]).all(1)) or \
           any(np.equal(transposed_data, [fill for _ in range(5)]).all(1))


def one(d_data: np.ndarray, b_data: np.ndarray) -> int:
    """
    To guarantee victory against the giant squid, figure out which board will win first.
    What will your final score be if you choose that board?
    """

    # If number is drawn, replace with {fill}
    fill = -1

    for draw in d_data:

        # Replace drawn number by -1
        b_data = np.where(b_data == draw, fill, b_data)

        for board in b_data:
            if bingo(board, fill):
                return np.sum(np.where(board == fill, 0, board)) * draw

    return -1


def two(d_data: np.ndarray, b_data: np.ndarray) -> int:
    """
    Figure out which board will win last. Once it wins, what would its final score be?
    """

    # If number is drawn, replace with {fill}
    fill = -1

    # List of completed bingo boards
    completed_idx = []

    for draw in d_data:

        # Replace drawn number by -1
        b_data = np.where(b_data == draw, fill, b_data)

        for board, i in zip(b_data, range(len(b_data))):
            if bingo(board, fill) and i not in completed_idx:
                completed_idx.append(i)

                if len(completed_idx) == len(b_data):
                    return np.sum(np.where(board == fill, 0, board)) * draw

    return -1


print(f"1. {one(draws, boards)}")
print(f"2. {two(draws, boards)}")
