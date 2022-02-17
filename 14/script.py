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


def two(data: list, mapping: dict, limit: int = 40) -> int:
    """
    Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result.
    What do you get if you take the quantity of the most common element and subtract the quantity of the least common
    element?

    Practically the first, but needs to be more efficient.
    """
    def recursive_count(template: dict, count: int = 1) -> dict:
        """
        Recursively keep track of how many of each pairing are present.
        """
        res = {}
        for (el, next_el), freq in template.items():
            new = mapping.get(el + next_el, 0)
            res[(el, new)] = res.get((el, new), 0) + freq
            res[(new, next_el)] = res.get((new, next_el), 0) + freq

        if count == limit:
            return res
        else:
            return recursive_count(res, count+1)

    def calc_freqs(template: dict) -> int:
        """
        Calculate the frequency of each individual element and calculate the difference between the most common and
        least common elements.
        """
        # Add one to the first and last element before dividing by 2 later.
        res = {
            data[0]: 1,
            data[-1]: 1,
        }
        for (el, next_el), freq in template.items():
            res[el] = (res.get(el, 0) + freq)
            res[next_el] = (res.get(next_el, 0) + freq)

        return int((max(res.values()) - min(res.values())) / 2)

    # Create frequency dictionary with template pairs.
    freq_dict = {}
    for tup in zip(data, data[1:]):
        freq_dict[tup] = freq_dict.get(tup, 0) + 1

    final_template = recursive_count(freq_dict)
    return calc_freqs(final_template)


print(f"1. {one(polymer_template, pair_insertion)}")
print(f"2. {two(polymer_template, pair_insertion)}")
