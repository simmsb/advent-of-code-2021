from functools import lru_cache
import itertools

positions = [1, 10]
scores = [0, 0]

die = itertools.cycle(range(1, 101))
n = 0

for i in itertools.cycle(range(len(positions))):
    a, b, c = next(die), next(die), next(die)
    n += 3
    positions[i] += a + b + c
    positions[i] = ((positions[i] - 1) % 10) + 1
    scores[i] += positions[i]
    if scores[i] >= 1000:
        break

print(min(scores) * n)


positions = [1, 10]
scores = [0, 0]

def step(pa, pb, sa, sb, t, n_un):
    if t:
        for s, mult in {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}.items():
            pa_ = pa + s
            pa_ = ((pa_ - 1) % 10) + 1
            sa_ = sa + pa_
            if sa_ >= 21:
                yield (True, mult * n_un)
            else:
                yield from step(pa_, pb, sa_, sb, not t, mult * n_un)

    else:
        for s, mult in {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}.items():
            pb_ = pb + s
            pb_ = ((pb_ - 1) % 10) + 1
            sb_ = sb + pb_
            if sb_ >= 21:
                yield (False, mult * n_un)
            else:
                yield from step(pa, pb_, sa, sb_, not t, mult * n_un)


a_s = 0
b_s = 0

for u, s in step(1, 10, 0, 0, True, 1):
    if u:
        a_s += s
    else:
        b_s += s

print(a_s, b_s)
