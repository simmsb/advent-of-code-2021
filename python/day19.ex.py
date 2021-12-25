from functools import reduce
import itertools

permutations = [
    lambda x, y, z: (x, y, z), # 0
    lambda x, y, z: (z, x, y), # 1
    lambda x, y, z: (y, z, x), # 2
    lambda x, y, z: (z, y, -x), # 3
    lambda x, y, z: (x, z, -y), # 4
    lambda x, y, z: (y, x, -z), # 5
    lambda x, y, z: (y, -z, -x), # 6
    lambda x, y, z: (z, -x, -y), # 7
    lambda x, y, z: (x, -y, -z), # 8
    lambda x, y, z: (y, -z, -x), # 9
    lambda x, y, z: (z, -x, -y), # 10
    lambda x, y, z: (x, -y, -z), # 11
    lambda x, y, z: (-y, z, -x), # 12
    lambda x, y, z: (-x, y, -z), # 13
    lambda x, y, z: (-z, x, -y), # 14
    lambda x, y, z: (-z, y, x), # 15
    lambda x, y, z: (-x, z, y), # 16
    lambda x, y, z: (-y, x, z), # 17
    lambda x, y, z: (-y, -z, x), # 18
    lambda x, y, z: (-z, -x, y), # 19
    lambda x, y, z: (-x, -y, z), # 20
    lambda x, y, z: (-z, -y, -x), # 21
    lambda x, y, z: (-x, -z, -y), # 22
    lambda x, y, z: (-y, -x, -z), # 23
]


permutations_inv = [
    lambda x, y, z: (x, y, z), # 0
    lambda z, x, y: (x, y, z), # 1
    lambda y, z, x: (x, y, z), # 2
    lambda z, y, x: (x, y, -z), # 3
    lambda x, z, y: (x, y, -z), # 4
    lambda y, x, z: (x, y, -z), # 5
    lambda y, z, x: (x, -y, -z), # 6
    lambda z, x, y: (x, -y, -z), # 7
    lambda x, y, z: (x, -y, -z), # 8
    lambda y, z, x: (x, -y, -z), # 9
    lambda z, x, y: (x, -y, -z), # 10
    lambda x, y, z: (x, -y, -z), # 11
    lambda y, z, x: (-x, y, -z), # 12
    lambda x, y, z: (-x, y, -z), # 13
    lambda z, x, y: (-x, y, -z), # 14
    lambda z, y, x: (-x, y, z), # 15
    lambda x, z, y: (-x, y, z), # 16
    lambda y, x, z: (-x, y, z), # 17
    lambda y, z, x: (-x, -y, z), # 18
    lambda z, x, y: (-x, -y, z), # 19
    lambda x, y, z: (-x, -y, z), # 20
    lambda z, y, x: (-x, -y, -z), # 21
    lambda x, z, y: (-x, -y, -z), # 22
    lambda y, x, z: (-x, -y, -z), # 23
]

def rotate(points, idx):
    out = []
    for p in points:
        out.append(permutations[idx](*p))

    return out

def rotate_inv(points, idx):
    out = []
    for p in points:
        out.append(permutations_inv[idx](*p))

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

                if len(points_union) > 1:
                    print(
                        f"found I think {i=} {rot=} {len(points_union)}",
                        sub(initial_b_rel, initial_a_rel),
                    )

                    offset_of_b_points = sub(initial_b_rel, initial_a_rel)

                    return offset_of_b_points, rot, set(relativise(a_points, a_points[0])) | set(relativise(b_points_rotated, offset_of_b_points))
    return None

def parse(l):
    return tuple([int(x) for x in l.split(",")])


with open("day19.ex.txt") as f:
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
    offsets_from = nx.Graph()
    found_relative_from = {}

    for p in itertools.permutations(zip(itertools.count(0), scanners)):
        it = iter(p)
        first_i, first = next(it)
        print(f"starting from {first_i=}")
        for i, scanner in it:
            if offsets_from.has_edge(first_i, i):
                continue
            r = match_up(first, scanner, i)
            if r is not None:
                offsets_from.add_edge(first_i, i, offset=r[0], rotation=r[1])
                found_relative_from[first_i, i] = r[2]


    rel_from_zero = {}
    points_from_zero = {}
    for a in range(len(scanners)):
        path = nx.shortest_path(offsets_from, 0, a)

        print(path)

        offs = (0, 0, 0)

        prev_rot = 0
        for x, y in itertools.pairwise(path):
            print(x, y, offsets_from[x][y]["offset"], offsets_from[x][y]["rotation"])
            off = rotate([offsets_from[x][y]["offset"]], prev_rot)[0]


            prev_rot = offsets_from[x][y]["rotation"]
            #offs = add(offs, offsets_from[x][y]["offset"])
            offs = add(offs, off)

        rel_from_zero[a] = offs

        prev_rot = 0
        points = scanners[a]

        # now just replay the rotati/ns in reverse
        for x, y in itertools.pairwise(path[::-1]):
            prev_rot = offsets_from[x][y]["rotation"]
            print("inverting rotation of", prev_rot)
            points = rotate(points, prev_rot)

        points = [add(point, rel_from_zero[a]) for point in points]

        points_from_zero[a] = sorted(points)


    # 1: 68,-1246,-43
    # 2: 1105,-1205,1229
    # 3: -92,-2380,-20
    # 4: -20,-1133,1061

    import pprint

    print(rel_from_zero)
    pprint.pp(points_from_zero)

    print(len(set(p for v in points_from_zero.values() for p in v)))

if __name__ == "__main__":
    go()
