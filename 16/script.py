from math import prod


literal_values = (
    sum, prod, min, max, None,
    lambda l: 1 if l[0] > l[1] else 0,
    lambda l: 1 if l[0] < l[1] else 0,
    lambda l: 1 if l[0] == l[1] else 0,
)


def one(b_str: str) -> int:
    """
    Decode the structure of your hexadecimal-encoded BITS transmission; what do you get if you add up the version
    numbers in all packets?
    """
    *_, version_sum = read_packet(b_str)
    return version_sum


def two(b_str: str) -> int:
    """
    What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?
    """
    literal, *_ = read_packet(b_str)
    return literal


def read_packet(b_str: str, version_sum: int = 0) -> (int, int, int):
    """
    Recursive search within a packet.
    """
    if "1" not in b_str:
        return "", 0

    version_sum += binary_to_int(b_str[:3])
    type_id = binary_to_int(b_str[3:6])

    # Literal value.
    if type_id == 4:
        literal, n_bits = read_literal_packet(b_str[6:])
    # Operator value.
    else:
        literal, n_bits, version_sum = read_operator_packet(b_str[6:], version_sum, type_id)

    return literal, n_bits + 6, version_sum


def read_literal_packet(b_str: str) -> (int, int):
    """
    Returns literal value as an integer and the number of bits handled.
    """
    def chunker(bit_seq: str, size: int = 5) -> list:
        """
        Groups bits together in chunks of 5.
        """
        return [bit_seq[pos:pos + size] for pos in range(0, len(bit_seq), size)]

    literal = ""
    n_bits = 0
    for chunk in chunker(b_str):
        literal += chunk[1:]
        n_bits += 5
        # Stop the loop if the last package is reached.
        if chunk[0] == "0":
            break

    return binary_to_int(literal), n_bits


def read_operator_packet(b_str: str, version_sum: int, type_id: int) -> (int, int, int):
    """
    Returns literal value as an integer and the number of bits handled.
    """
    literal_list = []

    # If 0 -> next 15 bits = total length.
    if b_str[0] == "0":
        total_length = binary_to_int(b_str[1:16]) + 16
        n_bits = 16
        while n_bits < total_length:
            literal, extra_bits, version_sum = read_packet(b_str[n_bits:], version_sum)
            literal_list.append(literal)
            n_bits += extra_bits

    # If 1 -> next 11 bits are n sub-packets.
    else:
        n_packets = binary_to_int(b_str[1:12])
        n_bits = 12
        while n_packets > 0:
            literal, extra_bits, version_sum = read_packet(b_str[n_bits:], version_sum)
            literal_list.append(literal)
            n_bits += extra_bits
            n_packets -= 1

    return literal_values[type_id](literal_list), n_bits, version_sum


def hex_to_binary(hex_str: str, padding_n: int) -> str:
    """
    Converts hex string to binary string.
    """
    return f"{int(hex_str, 16):0>{padding_n}b}"


def binary_to_int(binary_str: str) -> int:
    """
    Converts binary string to integer.
    """
    return int(binary_str, 2)


with open("data.txt", "r") as f:
    hex_data = f.read()
    binary_data = hex_to_binary(hex_data, len(hex_data) * 4)


print(f"1. {one(binary_data)}")
print(f"2. {two(binary_data)}")
