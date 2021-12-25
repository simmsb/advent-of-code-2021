import itertools

permutations = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (y, x, -z),
]


def rotate(points, idx):
    out = []
    for p in points:
        out.append(permutations[idx](*p))

    return out


def rotations_of(points):
    for idx in range(len(permutations)):
        yield rotate(points, idx), idx


def relativise(points, initial):
    x, y, z = initial

    out = []
    for x1, y1, z1 in points:
        out.append(tuple([x1 - x, y1 - y, z1 - z]))

    return out


def sub(a, b):
    return (
        b[0] - a[0],
        b[1] - a[1],
        b[2] - a[2],
    )


def add(a, b):
    return (
        b[0] + a[0],
        b[1] + a[1],
        b[2] + a[2],
    )


def match_up(a_points, b_points, i):
    for initial_a_rel in a_points:
        a_relative = relativise(a_points, initial_a_rel)

        for b_points_rotated, rot in rotations_of(b_points):
            for initial_b_rel in b_points_rotated:
                b_relative = relativise(b_points_rotated, initial_b_rel)

                points_union = set(a_relative) & set(b_relative)

                if len(points_union) >= 12:
                    # print(
                    #     f"found I think {i=} {rot=} {len(points_union)}",
                    #     sub(initial_b_rel, initial_a_rel),
                    # )

                    offset_of_b_points = sub(initial_b_rel, initial_a_rel)

                    return (
                        offset_of_b_points,
                        rot,
                    )
    return None


def parse(l):
    return tuple([int(x) for x in l.split(",")])


with open("day19.txt") as f:
    scanners = f.read().split("\n\n")

    scanners = [
        [parse(l) for l in scanner.strip().splitlines()[1:]] for scanner in scanners
    ]

import networkx as nx


def is_saturated(g, n):
    try:
        for i in range(n):
            if not nx.has_path(g, 0, i):
                return False
        return True
    except nx.NodeNotFound:
        return False


def go():
    import networkx as nx

    offsets_from = nx.DiGraph()
    has_been_aligned = {0}

    for first_i in itertools.cycle(range(len(scanners))):
        if len(has_been_aligned) == len(scanners):
            break
        # if is_saturated(offsets_from, len(scanners)):
        #     break
        # print(f"starting from {first_i=}")
        if first_i not in has_been_aligned:
            continue
        for i, scanner in enumerate(scanners):
            if i == first_i:
                continue
            if i in has_been_aligned:
                continue
            if offsets_from.has_edge(first_i, i):
                continue
            r = match_up(scanners[first_i], scanner, i)
            if r is not None:
                # rotate this resultset to be aligned with the first scanner
                # this should mean that when we check scans from relative to scanner 2
                # scanner 2 will be aligned to scanner 1
                scanners[i] = rotate(scanners[i], r[1])
                has_been_aligned.add(i)
                offsets_from.add_edge(first_i, i, offset=r[0])

    rel_from_zero = {}
    points_from_zero = {}
    for a in range(len(scanners)):
        path = nx.shortest_path(offsets_from, 0, a)

        # print(path)

        offs = (0, 0, 0)

        for x, y in zip(path, path[1:]):
            # print(x, y, offsets_from[x][y]["offset"])
            # offs = add(offs, offsets_from[x][y]["offset"])
            offs = add(offs, offsets_from[x][y]["offset"])

        # if len(path) > 1:
        #     offs = add(offs, offsets_from[path[-2]][path[-1]]["offset"])

        rel_from_zero[a] = offs  # rotate([offs], prev_rot)[0]

        points = scanners[a]
        points = [add(point, rel_from_zero[a]) for point in points]

        points_from_zero[a] = sorted(points)

    # 1: 68,-1246,-43
    # 2: 1105,-1205,1229
    # 3: -92,-2380,-20
    # 4: -20,-1133,1061

    # import pprint

    # print(rel_from_zero)
    # pprint.pp(points_from_zero)

    print(len(set(p for v in points_from_zero.values() for p in v)))

    v = 0
    for a, b in itertools.permutations(rel_from_zero.values(), 2):
        d = sub(a, b)
        v = max(v, sum(abs(x) for x in d))
    print(v)


if __name__ == "__main__":
    go()
