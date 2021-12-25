import numpy as np

inp = """
4764745784
4643457176
8322628477
7617152546
6137518165
1556723176
2187861886
2553422625
4817584638
3754285662
""".strip().split()

inp = [
    [int(x) for x in y]
    for y in inp
]


pattern = np.array([(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)])

state = np.array(inp)

flashes = 0

for i in range(1000):
    state += 1

    flashed = state == None

    while True:
        where_nine = state > 9
        new_flashed = flashed | where_nine
        where_nine &= ~flashed
        flashed = new_flashed

        if (state == 0).all():
            print(i + 1)
            raise Exception("lol")

        if not where_nine.any():
            break

        flashes += where_nine.sum()

        for middle in np.argwhere(where_nine):
            for pos in pattern + middle:
                x, y = pos

                if not 0 <= x < 10:
                    continue

                if not 0 <= y < 10:
                    continue

                state[x][y] += 1

        state[flashed] = 0

    if i == 99:
        print(flashes)

print(flashes)
