

def simulate(dx: int, dy: int, xrange, yrange):
    x, y = 0, 0

    max_y = 0

    while True:
        # print(x, y)
        if x in range(*xrange) and y in range(*yrange):
            return max_y

        if (dy < 0) and y < (min(yrange) - 10):
            return None

        max_y = max(y, max_y)
        x += dx
        y += dy
        if dx > 0:
            dx -= 1
        elif dx < 0:
            dx += 1

        dy -= 1


max_y = -9999
best_dx = None
best_dy = None
valid = set()
for dx in range(0, 450):
    for dy in range(0, 1000):
        for invx, invy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            r = simulate(dx * invx, dy * invy, (175,228), (-134,-78))
            # r = simulate(dx * invx, dy * invy, (20,31), (-10,-4))
            if r is not None:
                valid.add((dx * invx, dy * invy))
                if r > max_y:
                    max_y = r
                    best_dx = dx
                    best_dy = dy
                    # print(best_dx, best_dy, max_y)
print(best_dx, best_dy, max_y, len(valid))
