with open("data.txt") as f:
    nested_data = [[x.split(), y.split()] for x, y in [line.split(" | ") for line in f.read().split("\n")]]


def one(data: list, digits: tuple = (2, 4, 3, 7)) -> int:
    """
    In the output values, how many times do digits 1 (2), 4 (4), 7 (3), or 8 (7) appear?
    """

    return sum([len([value for value in output if len(value) in digits]) for _, output in data])


def split_chars(chars: str) -> list:
    """
    Splits string in separate strings (chars) in list.
    """
    return [char for char in chars]


def find_segments(line: list) -> dict:
    """
    Maps each segment of the seven-segment display to a char (letter).

        segment length  similar     unique
    1       8       1, 3        N                    1111
    2       6       2           Y                   2    3
    3       8       1, 3        N                   2    3
    4       7       4, 7        N                    4444
    5       4       5           Y                   5    6
    6       9       6           Y                   5    6
    7       7       4, 7        N                    7777
    """

    def find_one() -> str:
        """
        Returns the char (letter) linked to segment: 1.

        > difference between chars in no. 7 (unique) and  no. 1 (unique).
        """
        one_chars = split_chars(*[s for s in line if len(s) == 2])
        seven_chars = split_chars(*[s for s in line if len(s) == 3])
        return [c for c in seven_chars if c not in one_chars][0]

    def find_two() -> str:
        """
        Returns the char (letter) linked to segment: 2.

        > the char has a unique number of occurrences (6) in the line
        """
        flat_line = [c for li in line for c in li]
        return [c for c in flat_line if flat_line.count(c) == 6][0]

    def find_three(char_one: str) -> str:
        """
        Returns the char (letter) linked to segment: 3.

        > the char has the same number of occurrences (8) as char one. So it is the other one.
        """
        flat_line = [c for li in line for c in li]
        return [c for c in flat_line if flat_line.count(c) == 8 and c is not char_one][0]

    def find_four(char_seven: str) -> str:
        """
        Returns the char (letter) linked to segment: 4.

        > the char has the same number of occurrences (7) as char seven. So it is the other one.
        """
        flat_line = [c for li in line for c in li]
        return [c for c in flat_line if flat_line.count(c) == 7 and c is not char_seven][0]

    def find_five() -> str:
        """
        Returns the char (letter) linked to segment: 5.

        > the char has a unique number of occurrences (4) in the line
        """
        flat_line = [c for li in line for c in li]
        return [c for c in flat_line if flat_line.count(c) == 4][0]

    def find_six() -> str:
        """
        Returns the char (letter) linked to segment: 6.

        > the char has a unique number of occurrences (9) in the line.
        """
        flat_line = [c for li in line for c in li]
        return [c for c in flat_line if flat_line.count(c) == 9][0]

    def find_seven(char_one: str) -> str:
        """
        Returns the char (letter) linked to segment: 7.

        > chars in no. 4 (unique) and segment 1 using find_one() combined
        > compare these chars to chars of length 6 (segment 0, 6 or 9) (should all be in there)
        > difference between these two lists
        """
        four_chars = split_chars(*[s for s in line if len(s) == 4])
        nine_options = [split_chars(s) for s in line if len(s) == 6]
        nine_chars = [option for option in nine_options if all(c in option for c in four_chars + [char_one])][0]
        return [c for c in nine_chars if c not in four_chars + [char_one]][0]

    char_1 = find_one()
    char_7 = find_seven(char_1)

    return {
        1: find_one(),
        2: find_two(),
        3: find_three(char_1),
        4: find_four(char_7),
        5: find_five(),
        6: find_six(),
        7: find_seven(char_1),
    }


def decode_output(segments: dict, output: list) -> int:
    """
    Using the segments of the display, convert the output to 4-digit integer.
    """

    def convert(s: dict, d: list) -> str:
        """
        Convert list of chars (s in output) to the seven-segment display digit (0-9) as a string.
        """

        conversion_dict = {
            0: [s[1], s[2], s[3], s[5], s[6], s[7]],
            1: [s[3], s[6]],
            2: [s[1], s[3], s[4], s[5], s[7]],
            3: [s[1], s[3], s[4], s[6], s[7]],
            4: [s[2], s[3], s[4], s[6]],
            5: [s[1], s[2], s[4], s[6], s[7]],
            6: [s[1], s[2], s[4], s[5], s[6], s[7]],
            7: [s[1], s[3], s[6]],
            8: [s[1], s[2], s[3], s[4], s[5], s[6], s[7]],
            9: [s[1], s[2], s[3], s[4], s[6], s[7]],
        }

        for n in range(10):
            if set(d) == set(conversion_dict[n]):
                return str(n)

        return "ERROR"

    output_str = ""
    for digit in output:
        output_str += convert(segments, split_chars(digit))

    return int(output_str)


def two(data: list) -> int:
    """
    For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you
    get if you add up all of the output values?

    digit   length  similar     unique
    0       6       0, 6, 9     N
    1       2       1           Y
    2       5       2, 3, 5     N
    3       5       2, 3, 5     N
    4       4       4           Y
    5       5       2, 3, 5     N
    6       6       0, 6, 9     N
    7       3       7           Y
    8       7       8           Y
    9       6       0, 6, 9     N

    segment length  similar     unique
    1       8       1, 3        N                    1111
    2       6       2           Y                   2    3
    3       8       1, 3        N                   2    3
    4       7       4, 7        N                    4444
    5       4       5           Y                   5    6
    6       9       6           Y                   5    6
    7       7       4, 7        N                    7777

    """

    outputs = []
    for line, output in data:
        segments = find_segments(line)
        value = decode_output(segments, output)
        outputs.append(value)

    return sum(outputs)


print(f"1. {one(nested_data)}")
print(f"2. {two(nested_data)}")
