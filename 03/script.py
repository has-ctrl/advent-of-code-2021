import numpy as np

np_data = np.array([[int(bit) for bit in bit_str] for bit_str in np.loadtxt("data.txt", dtype=str)])


def binary_to_int(bit_str: list):
    """
    Convert list of bits to an integer.
    """
    res = 0
    for bit in bit_str:
        res = (res << 1) | bit

    return res


def one(data: np.ndarray) -> int:
    """
    Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them
    together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)
    """

    n_bits = len(data[0])
    gamma_rate = []
    epsilon_rate = []

    for pos in range(n_bits):
        pos_data = data[:, pos]
        n_0, n_1 = (pos_data == 0).sum(), (pos_data == 1).sum()

        g_bit = 0 if n_0 > n_1 else 1
        gamma_rate.append(g_bit)

        e_bit = 1 if n_0 > n_1 else 0
        epsilon_rate.append(e_bit)

    return binary_to_int(gamma_rate) * binary_to_int(epsilon_rate)


def two(data: np.ndarray) -> int:
    """
    Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating,
    then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in
    decimal, not binary.)
    """

    def loop(most_common: bool) -> int:
        """
        Loop through each bit for both the Oxygen generator rating (True) and CO2 scrubber rating (False).
        """
        n_bits = len(data[0])
        rating_list = np.copy(data)

        for pos in range(n_bits):
            if len(rating_list) <= 1:
                break

            pos_data = rating_list[:, pos]
            n_0, n_1 = (pos_data == 0).sum(), (pos_data == 1).sum()

            if most_common:
                bit = 1 if n_1 >= n_0 else 0
            else:
                bit = 0 if n_1 >= n_0 else 1

            rating_list = rating_list[rating_list[:, pos] == bit]

        return binary_to_int(rating_list[0])

    return loop(most_common=True) * loop(most_common=False)


print(f"1. {one(np_data)}")
print(f"2. {two(np_data)}")

