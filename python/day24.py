#!/usr/bin/env python3
import itertools

inp = """
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 16
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 0
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -5
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 2
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
""".strip().splitlines()

c = itertools.count(0)
# s_vars = []
# prog = []

# for ins in inp:
#     instr, *param = ins.split(" ")

#     if instr == "inp":
#         a, = param
#         v = next(c)
#         prog.append(f"{a} = s{v};")
#         s_vars.append(f"s{v}")
#     elif instr == "add":
#         a, b = param
#         prog.append(f"{a} += {b};")
#     elif instr == "mul":
#         a, b = param
#         prog.append(f"{a} *= {b};")
#     elif instr == "div":
#         a, b = param
#         prog.append(f"{a} /= {b};")
#     elif instr == "mod":
#         a, b = param
#         prog.append(f"{a} %= {b};")
#     elif instr == "eql":
#         a, b = param
#         prog.append(f"{a} = {a} == {b};")

# print("int main(int argc, char **argv) {")
# for i, s_var in enumerate(s_vars):
#     # print(f"for (int {s_var} = 9; {s_var} > 0; {s_var}--) {{")
#     print(f"int {s_var} = atoi(argv[{i + 1}]);")

# print("\n".join(f"int {v} = 0;" for v in "wxyz"))
# print("\n".join(prog))
# f_string = "%d " * len(s_vars)
# s_vars_fmt = ", ".join(s_vars)
# print(f"if (z == 0) {{ printf(\"f: {f_string}\\n\", {s_vars_fmt}); break; }}")
# print("}")
# print("}" * len(s_vars))

def read(state, v):
    try:
        x = int(v)
        return x
    except ValueError:
        return state[v]

# import z3

# s = z3.Solver()
# counter = itertools.count(0)
#
num = input()
num_s = iter(num)

def exec(inp, state):
    instr, *param = inp.split(" ")

    if instr == "inp":
        a, = param
        state[a] = int(next(num_s))
    elif instr == "add":
        a, b = param
        av = read(state, a)
        bv = read(state, b)
        state[a] = av + bv
    elif instr == "mul":
        a, b = param
        av = read(state, a)
        bv = read(state, b)
        state[a] = av * bv
    elif instr == "div":
        a, b = param
        av = read(state, a)
        bv = read(state, b)
        state[a] = av // bv
    elif instr == "mod":
        a, b = param
        av = read(state, a)
        bv = read(state, b)
        state[a] = av % bv
    elif instr == "eql":
        a, b = param
        av = read(state, a)
        bv = read(state, b)
        state[a] = int(av == bv)

# def simpl_pass(s):
#     if isinstance(s, int):
#         return s
#     return z3.simplify(s)

state = {v: 0 for v in "wxyz"}

for ins in inp:
    exec(ins, state)
    print(state)

# for v in state.values():
#     s.add(state["z"] == 0)

# print(s.check())
