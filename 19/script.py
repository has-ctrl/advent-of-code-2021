def calc_distance(c1: tuple[int, int, int], c2: [tuple[int, int, int]]) -> int:
    """
    Calculate the Manhattan distance between two 3d coordinates.
    """
    return int(abs(c1[0] - c2[0] + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])))


def align(known_beacons: set[tuple[int, int, int]], unaligned_beacons: list[tuple[int, int, int]]) \
        -> tuple[[set[int, int, int]], tuple[int, int, int]] | tuple[None, None]:
    """
    Try to align the known beacons with the unaligned beacons.
    """
    def diffs(poses) -> list[tuple[int, int, int]]:
        """
        Calculate differences between the poses.
        """
        return [
            (x1 - x0, y1 - y0, z1 - z0)
            for (x0, y0, z0), (x1, y1, z1)
            in zip(poses, poses[1:])
        ]

    for axis in {0, 1, 2}:
        known_sorted = sorted(known_beacons, key=lambda pos: pos[axis])
        unaligned_beacons.sort(key=lambda pos: pos[axis])
        known_diffs = diffs(known_sorted)
        unaligned_diffs = diffs(unaligned_beacons)
        intersection = set(known_diffs) & set(unaligned_diffs)
        if intersection:
            diff = intersection.pop()
            kx, ky, kz = known_sorted[known_diffs.index(diff)]
            ux, uy, uz = unaligned_beacons[unaligned_diffs.index(diff)]
            ox, oy, oz = (ux - kx, uy - ky, uz - kz)
            moved = {(x - ox, y - oy, z - oz) for (x, y, z) in unaligned_beacons}
            matches = known_beacons & moved
            if len(matches) >= 12:
                return moved, (ox, oy, oz)

    return None, None


def turn(beacon: tuple[int, int, int], axis1: int, sign1: int, axis2: int, sign2: int) -> tuple[int, int, int]:
    """
    Turn beacon with coordinates {beacon} given the axes and signs (pos/neg).
    """
    axis3 = 3 - (axis1 + axis2)
    sign3 = 1 if (((axis2 - axis1) % 3 == 1) ^ (sign1 != sign2)) else -1
    return beacon[axis1] * sign1, beacon[axis2] * sign2, beacon[axis3] * sign3


def turn_and_align(known_beacons: set[tuple[int, int, int]], unknown_beacons: list[tuple[int, int, int]]) \
        -> tuple[list[tuple[int, int, int]], tuple[int, int, int]] | tuple[None, None]:
    """
    Update beacon map by trying to turn and align the unknown beacons.
    """
    for axis1 in {0, 1, 2}:
        for sign1 in [1, -1]:
            for axis2 in {0, 1, 2} - {axis1}:
                for sign2 in [1, -1]:
                    unaligned_beacons = [turn(beacon, axis1, sign1, axis2, sign2) for beacon in unknown_beacons]
                    aligned_beacons, scanner = align(known_beacons, unaligned_beacons)
                    if aligned_beacons:
                        return aligned_beacons, scanner
    return None, None


def find_all_beacons_and_scanners(data: list[list[tuple[int, int, int]]]) -> \
        tuple[set[tuple[int, int, int]], list[tuple[int, int, int]]]:
    """
    Tries to turn and align all beacons to construct the entire map and return it.
    """
    known_scanners = [(0, 0, 0)]
    known_beacons = set(data[0])
    unknown_beacon_readings = data[1:]
    while unknown_beacon_readings:
        for unknown_beacons in unknown_beacon_readings:
            beacons, scanner = turn_and_align(known_beacons, unknown_beacons)
            if beacons:
                unknown_beacon_readings.remove(unknown_beacons)
                known_beacons.update(beacons)
                known_scanners.append(scanner)
    return known_beacons, known_scanners


def one(data: list[list[tuple[int, int, int]]]) -> int:
    """
    Assemble the full map of beacons. How many beacons are there?
    """
    known_beacons, _ = find_all_beacons_and_scanners(data)
    return len(known_beacons)


def two(data) -> int:
    """
    What is the largest Manhattan distance between any two scanners?
    """
    _, known_scanners = find_all_beacons_and_scanners(data)

    max_distance = 0
    for c1 in known_scanners:
        for c2 in known_scanners[1:]:
            distance = calc_distance(c1, c2)
            max_distance = max(distance, max_distance)
    return max_distance


with open("data.txt", "r") as f:
    input_data = [[tuple(int(n) for n in r.split(",")) for r in b.split("\n")[1:]] for b in f.read().split("\n\n")]


print(f"1. {one(input_data)}")
print(f"2. {two(input_data)}")
