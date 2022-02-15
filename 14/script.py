from collections import Counter


with open("data.txt") as f:
    polymer_template = list(f.readline().strip("\n"))
    pair_insertion = {m[0]: m[1] for m in [match.split(" -> ") for match in f.read()[1:].split("\n")]}


def one(data: list, mapping: dict, limit: int = 10) -> int:
    """
    Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result.
    What do you get if you take the quantity of the most common element and subtract the quantity of the least common
    element?
    """

    def recursive_insertion(template: list, count: int = 1) -> list:
        """
        Recursively insert the correct char based on the mapping.
        """
        res = []
        for el, next_el in zip(template, template[1:]):
            res.extend([el, mapping.get(el + next_el)])

        # Add last element to the list.
        res += [template[-1]]
        if count == limit:
            return res
        else:
            return recursive_insertion(res, count+1)

    final_template = recursive_insertion(data)
    freqs = [freq for _, freq in Counter(final_template).most_common()]
    return max(freqs) - min(freqs)


def two(data: list) -> int:
    """
    Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result.
    What do you get if you take the quantity of the most common element and subtract the quantity of the least common
    element?

    Practically the first, but needs to be more efficient.
    """
    return 0


print(f"1. {one(polymer_template, pair_insertion)}")
print(f"2. {two(polymer_template)}")
