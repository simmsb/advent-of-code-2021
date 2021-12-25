import networkx

import itertools

with open("day8.txt") as f:
    inp = f.readlines()


def parse(inp: str):
    a, b = inp.split("|")
    a = a.strip().split()
    b = b.strip().split()

    return a, b


aaa = [parse(x) for x in inp]

pos_to_numbers = {
    frozenset({"A", "B", "C", "E", "F", "G"}): 0,
    frozenset({"C", "F"}): 1,
    frozenset({"A", "C", "D", "E", "G"}): 2,
    frozenset({"A", "C", "D", "F", "G"}): 3,
    frozenset({"B", "C", "D", "F"}): 4,
    frozenset({"A", "B", "D", "F", "G"}): 5,
    frozenset({"A", "B", "D", "E", "F", "G"}): 6,
    frozenset({"A", "C", "F"}): 7,
    frozenset({"A", "B", "C", "D", "E", "F", "G"}): 8,
    frozenset({"A", "B", "C", "D", "F", "G"}): 9,
}


def solve(a, b):

    # canonical positions == example

    combined = [*a, *b]

    # import z3
    # s = z3.Solver()

    # vars = A, B, C, D, E, F, G = [z3.Int(c) for c in "ABCDEFG"]

    assignments = Ap, Bp, Cp, Dp, Ep, Fp, Gp = [set("abcdefg") for _ in "ABCDEFG"]

    one = next((x for x in combined if len(x) == 2), None)
    if one is not None:
        for p in (Cp, Fp):
            p.intersection_update(one)
        # r = []
        # for comb in itertools.permutations((C, F), 2):
        #     r.append(z3.And(*[v == "ABCDEFG".index(k.upper()) for v, k in zip(comb, one)]))
        # s.add(z3.Or(*r))

    four = next((x for x in combined if len(x) == 4), None)
    if four is not None:
        for p in (Bp, Cp, Dp, Fp):
            p.intersection_update(four)
        # r = []
        # for comb in itertools.permutations((B, C, D, F), 4):
        #     r.append(z3.And(*[v == "ABCDEFG".index(k.upper()) for v, k in zip(comb, four)]))
        # s.add(z3.Or(*r))

    seven = next((x for x in combined if len(x) == 7), None)
    if seven is not None:
        for p in (Ap, Cp, Fp):
            p.intersection_update(seven)
        # r = []
        # for comb in itertools.permutations((A, C, F), 3):
        #     r.append(z3.And(*[v == "ABCDEFG".index(k.upper()) for v, k in zip(comb, seven)]))
        # s.add(z3.Or(*r))

    eight = next((x for x in combined if len(x) == 8), None)
    if eight is not None:
        for p in (Ap, Bp, Cp, Dp, Ep, Fp):
            p.intersection_update(eight)
        # r = []
        # for comb in itertools.permutations((A, B, C, D, E, F), 6):
        #     r.append(z3.And(*[v == "ABCDEFG".index(k.upper()) for v, k in zip(comb, eight)]))
        # s.add(z3.Or(*r))
        #

    def try_a(assn: tuple[str]):
        # if assn != tuple("deafgbc"):
        #     return False
        for o in b:  # word: abcddef
            # print(o, ["ABCDEFG"[assn.index(c)] for c in o])
            # print(frozenset("ABCDEFG"[assn.index(c)] for c in o))
            if frozenset("ABCDEFG"[assn.index(c)] for c in o) not in pos_to_numbers:
                return False
        return True

    for assignment in itertools.product(*assignments):
        if len(set(assignment)) != len(assignment):
            continue

        if try_a(assignment):
            break
    else:
        print("it's fucked mate", assignment, assignments)
        return

    n = int(
        "".join(
            str(pos_to_numbers[frozenset("ABCDEFG"[assignment.index(c)] for c in o)])
            for o in b
        )
    )

    return n

    # # g = networkx.Graph()

    # # for n, s in zip("ABCDEFG", assignments):
    # #     for c in s:
    # #         g.add_edge(n, c)

    # # print(networkx.maximal_matching(g))

    # six_canonicals = [
    #     (Ap, Bp, Cp, Ep, Fp, Gp),
    #     (Ap, Bp, Dp, Ep, Fp, Gp),
    #     (Ap, Bp, Cp, Dp, Fp, Gp)
    # ]
    # for entry in (x for x in combined if len(x) == 6):
    #     for canonical_e in six_canonicals:
    #         pass
    #     # for p in canonical_e:
    #     #     p.intersection_update(entry)
    #     # r = []
    #     # for comb in itertools.permutations(canonical_e, len(canonical_e)):
    #     #     r.append(z3.And(*[v == "ABCDEFG".index(k.upper()) for v, k in zip(comb, entry)]))
    #     # s.add(z3.Or(*r))

    # five_canonicals = [
    #     (Ap, Cp, Dp, Ep, Gp),
    #     (Ap, Cp, Dp, Fp, Gp),
    #     (Ap, Bp, Dp, Fp, Gp)
    # ]
    # for entry in (x for x in combined if len(x) == 5):
    #     for canonical_e in five_canonicals:
    #         pass
    #     # for p in canonical_e:
    #     #     p.intersection_update(entry)
    #     # r = []
    #     # for comb in itertools.permutations(canonical_e, len(canonical_e)):
    #     #     r.append(z3.And(*[v == "ABCDEFG".index(k.upper()) for v, k in zip(comb, entry)]))
    #     # s.add(z3.Or(*r))
    #     #
    # print(assignments)

    # # for v in vars:
    # #     s.add(v >= 0, v < len("ABCDEFG"))

    # # print(s)

    # s.add(z3.Distinct(*vars))

    # assert s.check() == z3.sat, "fuck"

    # m = s.model()

    # for o in b:
    #     print([m[vars["ABCDEFG".index(x.upper())]].as_long() for x in o])


total = 0
for x, y in aaa:
    total += solve(x, y)

print(total)
