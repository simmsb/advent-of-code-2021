import networkx as nx
from collections import defaultdict

inp = """
hl-WP
vl-fo
vl-WW
WP-start
vl-QW
fo-wy
WW-dz
dz-hl
fo-end
VH-fo
ps-vl
FN-dz
WP-ps
ps-start
WW-hl
end-QW
start-vl
WP-fo
end-FN
hl-QW
WP-dz
QW-fo
QW-dz
ps-dz
""".strip().split()

g = nx.Graph([x.split("-") for x in inp])

def canvisit(c, visited, used_small):
    if c in ("start", "end"):
        return visited[c] < 1, False
    if c.islower():
        if used_small:
            return visited[c] < 1, False
        return visited[c] < 2, visited[c] == 1
    return True, False

def traverse(n, path, visited, completed, used_small):
    to_visit = sorted(list(g[n]))
    for n in to_visit:
        can_visit, tused_small = canvisit(n, visited, used_small)
        if not can_visit:
            continue

        tvisited = visited.copy()
        tvisited[n] += 1

        if n == 'end':
            completed.append(path + ['end'])
        else:
            traverse(n, path + [n], tvisited, completed, tused_small | used_small)

completed = []
traverse('start', ['start'], defaultdict(lambda: 0, {'start': 1}), completed, False)
print(len(completed))
