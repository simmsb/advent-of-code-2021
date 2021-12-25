import numpy as np

def parse_line(s: str):
    s, d = s.split("->")
    sx, sy = s.strip().split(",")
    dx, dy = d.strip().split(",")
    return (int(sx), int(sy)), (int(dx), int(dy))

def find_largest(lines: list[tuple[tuple[int, int], tuple[int, int]]]):
    x = max(x for ((a, _), (b, _)) in lines
            for x in (a, b)) + 1
    y = max(y for ((_, a), (_, b)) in lines
            for y in (a, b)) + 1

    return x, y

def add_line(arr, line: tuple[tuple[int, int], tuple[int, int]]):
    (x0, y0), (x1, y1) = line

    if x0 == x1:
        if y1 < y0:
            y0, y1 = y1, y0
        for y in range(y0, y1 + 1):
            arr[y][x0] += 1
    elif y0 == y1:
        if x1 < x0:
            x0, x1 = x1, x0
        for x in range(x0, x1 + 1):
            arr[y0][x] += 1
    elif (y1 - y0) == (x1 - x0):
        print("huh", x0, y0, x1, y1, (x1 - x0))
        d = x1 - x0
        o = 1
        if d < 0:
            d = -d
            o = -1
        for n in range(d + 1):
            arr[y0 + n * o][x0 + n * o] += 1
    elif (y1 - y0) == -(x1 - x0):
        print("huh", x0, y0, x1, y1, (x1 - x0))
        d = x1 - x0
        o = 1
        if d < 0:
            d = -d
            o = -1
        for n in range(d + 1):
            arr[y0 - n * o][x0 + n * o] += 1

with open("day5.txt") as f:
    lines = [parse_line(l) for l in f.readlines()]

lenx, leny = find_largest(lines)
print(lenx, leny)
arr = np.zeros((leny, lenx))

for line in lines:
    add_line(arr, line)


print(arr)
print(sum(1 for x in np.nditer(arr) if x > 1))
