import matplotlib.pyplot as plt
from typing import Union


with open("data.txt") as f:
    input_data = f.read()
    dots_str = [s.split(",") for s in input_data.split("\n\n")[0].split("\n")]
    folds_str = [s.replace("fold along ", "").split("=") for s in input_data.split("\n\n")[1].split("\n")]
    dots_and_folds = [(int(x), int(y)) for x, y in dots_str], [(x, int(y)) for x, y in folds_str]


def one(data: tuple, only_first: bool = True) -> Union[int, str]:
    """
    How many dots are visible after completing just the first fold instruction on your transparent paper?
    """
    dots, folds = data

    for axis, line in folds:
        dots_state = set()
        for x, y in dots:
            if axis == "x":
                # If the dot is on the left side of the fold, do not change anything.
                if x < line:
                    dots_state.add((x, y))
                # If dot on right side of fold, subtract the X from the maximum width (2 * the fold line).
                else:
                    dots_state.add((line*2 - x, y))
            elif axis == "y":
                # If the dot is on the upper side of the fold, do not change anything.
                if y < line:
                    dots_state.add((x, y))
                # If dot on lower side of fold, subtract the Y from the maximum width (2 * the fold line).
                else:
                    dots_state.add((x, line*2 - y))

        dots = dots_state
        if only_first:
            return len(dots)

    # Proper printing instructions.
    plt.figure(figsize=(6, 1))
    plt.gca().invert_yaxis()
    plt.scatter(*zip(*dots))
    plt.show()
    return "See figure!"


def two(data: tuple) -> int:
    """
    What code do you use to activate the infrared thermal imaging camera system?
    """
    return one(data, only_first=False)


print(f"1. {one(dots_and_folds)}")
print(f"2. {two(dots_and_folds)}")
