import numpy as np

np_data = np.loadtxt("data.txt", dtype=str)

CHARS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def one(data: np.ndarray) -> (int, list):
    """
    Find the first illegal character in each corrupted line of the navigation subsystem. What is the total syntax error
    score for those errors?
    """
    error_score = 0
    corrupted_idx = []
    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    for i, line in enumerate(data):
        opening_chars = []
        for char in line:
            # If opening of a chunk, add to list.
            if char in CHARS.keys():
                opening_chars.append(char)
            # If closure of a chunk, check if valid.
            else:
                # If correct closure, delete it from the opening_chars list.
                if char is CHARS.get(opening_chars[-1]):
                    opening_chars = opening_chars[:-1]
                # If incorrect closure, add error score.
                else:
                    error_score += points.get(char)
                    corrupted_idx.append(i)
                    break

    return error_score, corrupted_idx


def two(data: np.ndarray) -> int:
    """
    Find the completion string for each incomplete line, score the completion strings, and sort the scores.
    What is the middle score?
    """

    def calc_score(completion_list: list) -> int:
        """
        Calculate the score autocompletion score. Start with a total score of 0. Then, for each character, multiply the
        total score by 5 and then increase the total score by the point value given for the character.
        """
        total_score = 0
        for c in completion_list:
            total_score = total_score * 5 + points.get(CHARS.get(c))
        return total_score

    _, corrupted_idx = one(data)
    scores = []
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    for i, line in enumerate(data):
        if i not in corrupted_idx:
            opening_chars = []
            for char in line:
                # If opening of a chunk, add to list.
                if char in CHARS.keys():
                    opening_chars.append(char)
                # No need for check anymore.
                else:
                    opening_chars = opening_chars[:-1]

            scores.append(calc_score(list(reversed(opening_chars))))

    return int(np.median(sorted(scores)))


print(f"1. {one(np_data)[0]}")
print(f"2. {two(np_data)}")
