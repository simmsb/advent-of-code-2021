from __future__ import annotations
import itertools
import math

from dataclasses import dataclass
from typing import Any


@dataclass
class TreeZipper:
    inner: Any
    path: list[int]

    def up(self):
        if self.path:
            return TreeZipper(self.inner, self.path[:-1]), self.path[-1]
        return None

    def get(self):
        v = self.inner
        for p in self.path:
            v = v[p]

        return v

    def set(self, x):
        v = self.inner
        for p in self.path[:-1]:
            v = v[p]
        v[self.path[-1]] = x

    def try_left(self):
        v = self.get()
        if isinstance(v, list):
            return TreeZipper(self.inner, self.path + [0])
        return None

    def try_right(self):
        v = self.get()
        if isinstance(v, list):
            return TreeZipper(self.inner, self.path + [1])
        return None


class Whoop(Exception):
    pass


def do_reduce_exp(v: TreeZipper, depth):
    if depth == 4 and isinstance(v.get(), list):
        # print("exploding")
        l, r = v.get()
        v.set(0)

        l_v = v
        came_from_left = False
        dont_go = False
        while True:
            # print("left", l_v, l_v.get())
            if (l_v_n := l_v.try_left()) != None and not came_from_left:
                l_v = l_v_n
                break
            elif (l_v_n_v := l_v.up()) != None:
                # if we can up and didn't go left, do so
                l_v = l_v_n_v[0]
                came_from_left = l_v_n_v[1] == 0
            else:
                dont_go = True
                # if we did nothing, we have to have reached the top and we were already from the left
                break
        if not dont_go:
            while True:
                if (l_v_n := l_v.try_right()) != None:
                    l_v = l_v_n
                # try to go down and to the left
                if isinstance(l_v.get(), int):
                    # if it's an int, add and quit
                    l_v.set(l_v.get() + l)
                    break

        l_v = v
        came_from_right = False
        dont_go = False
        while True:
            # print("right", l_v, l_v.get())
            if (l_v_n := l_v.try_right()) != None and not came_from_right:
                l_v = l_v_n
                break
            elif (l_v_n_v := l_v.up()) != None:
                # if we can up and didn't go left, do so
                l_v = l_v_n_v[0]
                came_from_right = l_v_n_v[1] == 1
            else:
                # if we did nothing, we have to have reached the top, bail
                dont_go = True
                break

        if not dont_go:
            while True:
                if (l_v_n := l_v.try_left()) != None:
                    l_v = l_v_n
                # try to go down and to the left
                if isinstance(l_v.get(), int):
                    # if it's an int, add and quit
                    l_v.set(l_v.get() + r)
                    break
        raise Whoop()


    if (l_v := v.try_left()) != None:
        do_reduce_exp(l_v, depth + 1)

    if (r_v := v.try_right()) != None:
        do_reduce_exp(r_v, depth + 1)

def do_reduce_splt(v: TreeZipper):
    n_v = v.get()
    if isinstance(n_v, int):
        if n_v >= 10:
            # print("splitting")
            l_v = math.floor(n_v / 2)
            r_v = math.ceil(n_v / 2)
            v.set([l_v, r_v])
            raise Whoop()

    # otherwise, go and reduce both sides
    if (l_v := v.try_left()) != None:
        do_reduce_splt(l_v)

    if (r_v := v.try_right()) != None:
        do_reduce_splt(r_v)

def iter_red(l):
    # print("doing", l)
    while True:
        t = TreeZipper(l, [])
        try:
            # print(l)
            do_reduce_exp(t, 0)
            do_reduce_splt(t)
        except Whoop:
            pass
        else:
            print("did nothing")
            return


def do_mag(v: TreeZipper):
    if isinstance(v.get(), int):
        return v.get()

    return 3 * do_mag(v.try_left()) + 2 * do_mag(v.try_right())


inp = [
[[[[7,1],[0,0]],[6,[8,2]]],[8,[3,8]]],
[[[3,6],[9,4]],[[[5,9],5],[8,0]]],
[[[2,2],2],[1,[[1,6],7]]],
[[[[0,9],7],[[3,2],8]],[6,[7,9]]],
[[[[4,1],6],[[7,6],[2,2]]],[[[1,1],9],4]],
[[[8,[3,7]],3],[[4,4],[[9,1],[3,5]]]],
[[4,[8,2]],[1,[0,5]]],
[8,[8,7]],
[[[[2,2],7],[3,[4,5]]],[[4,6],[[2,5],4]]],
[[[5,5],[[5,1],3]],[[2,[8,2]],[[6,9],[1,5]]]],
[0,7],
[[[[5,1],3],[8,[5,3]]],7],
[[5,[2,[0,6]]],[[[5,5],2],[9,[8,0]]]],
[[[[3,4],2],0],4],
[[[[5,3],[2,7]],6],[[4,0],[9,[7,2]]]],
[[[3,[2,5]],[3,3]],7],
[[[[5,1],1],[4,8]],[[5,[8,3]],2]],
[[4,[[8,1],[8,5]]],[[[4,1],0],6]],
[[[5,5],[5,9]],[0,[[6,8],[0,1]]]],
[4,[[[7,9],4],0]],
[[[[0,1],7],[[3,6],5]],[8,[5,[6,1]]]],
[[[7,7],[8,0]],[6,[8,[7,9]]]],
[[[9,2],1],6],
[[[4,4],[2,[5,0]]],[[[2,6],6],[5,[4,3]]]],
[[2,[[4,7],5]],1],
[[8,7],[[[2,0],7],[1,[0,3]]]],
[[9,[[9,3],[9,5]]],[[8,7],[[4,1],[6,5]]]],
[[3,4],[[9,4],5]],
[[5,[[8,3],5]],1],
[[0,[[9,0],[3,2]]],[2,[7,[5,1]]]],
[[9,[[9,5],[8,6]]],[[4,4],[[3,8],[1,6]]]],
[[[1,[5,2]],9],[[4,6],[3,[8,0]]]],
[[1,7],[[1,7],9]],
[[[[3,4],3],[[7,5],[9,1]]],[[[5,0],[3,0]],[[7,9],6]]],
[[[7,2],[[1,0],[5,6]]],[[[3,7],[8,9]],6]],
[[[[1,1],1],[[8,6],[9,8]]],[[[1,8],4],[8,9]]],
[[[8,9],0],3],
[[[1,7],[1,[3,9]]],[6,[0,[8,5]]]],
[[0,5],[6,5]],
[[[[6,8],[4,5]],[[7,4],6]],[[3,6],5]],
[[8,[[0,9],8]],[9,[7,[7,9]]]],
[0,[[[7,1],2],[[0,4],4]]],
[[0,[[9,1],5]],[1,4]],
[3,4],
[[[9,3],[1,3]],[[[4,8],3],[[1,3],[9,0]]]],
[[[[5,1],7],[[9,2],8]],[[[6,8],[5,4]],[0,1]]],
[8,[[1,[3,0]],[[7,9],4]]],
[[[6,4],[[2,9],[9,0]]],[7,[[0,0],3]]],
[[3,[[9,6],6]],2],
[[5,[[3,1],[7,5]]],[[[6,7],9],[[4,6],[5,2]]]],
[[[4,[6,5]],8],[[6,[8,0]],[[9,3],3]]],
[[[[4,9],[2,8]],9],[[[5,0],0],[[3,4],[2,8]]]],
[[3,[7,1]],[9,[[1,8],7]]],
[[9,1],[0,[[0,7],[7,1]]]],
[[7,[0,[7,6]]],[[[5,3],1],[6,[4,5]]]],
[8,[[[2,1],[6,9]],[[3,3],[4,6]]]],
[0,[7,[3,0]]],
[[[[1,6],3],[5,[8,0]]],[[[6,6],7],1]],
[[[7,[8,3]],3],[[[2,8],5],[0,[9,5]]]],
[[[[5,1],4],[[1,2],1]],7],
[[[3,[7,5]],7],3],
[[9,[6,[1,1]]],[[[4,1],[2,2]],[[9,5],[7,7]]]],
[2,7],
[[[9,[8,6]],[[9,0],[6,5]]],[[[6,7],5],[[7,7],[2,3]]]],
[[[0,[6,4]],2],[4,[7,[7,5]]]],
[[[[6,1],[9,1]],[[6,1],9]],[[2,6],0]],
[[0,[[1,8],[3,5]]],[4,[[8,2],[4,2]]]],
[[[[9,3],[4,2]],2],[[[2,1],[7,1]],[4,8]]],
[[[3,[0,2]],3],8],
[[[4,[4,9]],9],[[[4,4],5],9]],
[[[[8,2],7],9],[[[1,0],[3,8]],[[7,7],0]]],
[[[3,2],[9,7]],[[9,[8,2]],[[5,5],3]]],
[[[7,[3,1]],[[8,3],1]],[[[8,6],[7,0]],4]],
[[9,[[9,1],5]],[[4,[1,1]],2]],
[[[[7,4],[0,3]],7],[8,[6,[3,3]]]],
[5,5],
[[6,7],[1,[7,[8,1]]]],
[[1,[0,4]],7],
[[[4,0],[[0,1],[2,2]]],[9,[[9,9],[3,0]]]],
[[[6,0],[[8,6],3]],[[5,1],[[8,1],[2,7]]]],
[[[[8,3],7],5],[9,[[5,1],8]]],
[[[[4,0],[5,2]],[[0,0],7]],2],
[[[[0,1],6],2],[[8,2],6]],
[[[[2,4],1],[[6,7],9]],[[[1,6],9],3]],
[[5,5],[[8,[7,7]],[5,8]]],
[[6,[[9,2],[9,7]]],[[[8,5],[4,4]],7]],
[[[9,[7,7]],[6,0]],[7,[[8,7],[1,2]]]],
[[7,[6,2]],[[9,[5,2]],[1,4]]],
[[[7,[5,9]],[[3,9],[4,5]]],[0,6]],
[[9,[8,[2,2]]],[[9,7],[1,1]]],
[[[[2,3],4],[[4,8],9]],[[9,[8,6]],[[0,9],0]]],
[[0,[[9,3],0]],[8,8]],
[[[[2,9],6],[[2,8],9]],[[[0,5],6],[[6,1],7]]],
[[9,[[8,3],[5,8]]],[[7,[3,0]],3]],
[[[4,[4,2]],0],1],
[[[[9,6],[5,8]],[6,2]],[[[8,0],[7,0]],[[5,6],4]]],
[[[8,0],[[4,3],[7,4]]],[[3,[7,9]],[[7,3],6]]],
[[3,[5,[0,3]]],[5,4]],
[[[[1,2],[6,3]],1],[[7,[5,2]],[[8,8],7]]],
[[4,[[8,0],[7,1]]],[[8,[8,0]],[[1,5],3]]]

]

inp = [
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
[[[5,[2,8]],4],[5,[[9,9],0]]],
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
[[[[5,4],[7,7]],8],[[8,3],8]],
[[9,3],[[9,9],[6,[4,9]]]],
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
]

# inp = [
# [[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]
# ]


def do_add(l):
    it = iter(l)
    x = next(it)
    iter_red(x)

    for y in it:
        x = [x, y]
        iter_red(x)

    return x


out = do_add(inp)
print(out)
print(do_mag(TreeZipper(out, [])))
import copy
inp = [
[[[[7,1],[0,0]],[6,[8,2]]],[8,[3,8]]],
[[[3,6],[9,4]],[[[5,9],5],[8,0]]],
[[[2,2],2],[1,[[1,6],7]]],
[[[[0,9],7],[[3,2],8]],[6,[7,9]]],
[[[[4,1],6],[[7,6],[2,2]]],[[[1,1],9],4]],
[[[8,[3,7]],3],[[4,4],[[9,1],[3,5]]]],
[[4,[8,2]],[1,[0,5]]],
[8,[8,7]],
[[[[2,2],7],[3,[4,5]]],[[4,6],[[2,5],4]]],
[[[5,5],[[5,1],3]],[[2,[8,2]],[[6,9],[1,5]]]],
[0,7],
[[[[5,1],3],[8,[5,3]]],7],
[[5,[2,[0,6]]],[[[5,5],2],[9,[8,0]]]],
[[[[3,4],2],0],4],
[[[[5,3],[2,7]],6],[[4,0],[9,[7,2]]]],
[[[3,[2,5]],[3,3]],7],
[[[[5,1],1],[4,8]],[[5,[8,3]],2]],
[[4,[[8,1],[8,5]]],[[[4,1],0],6]],
[[[5,5],[5,9]],[0,[[6,8],[0,1]]]],
[4,[[[7,9],4],0]],
[[[[0,1],7],[[3,6],5]],[8,[5,[6,1]]]],
[[[7,7],[8,0]],[6,[8,[7,9]]]],
[[[9,2],1],6],
[[[4,4],[2,[5,0]]],[[[2,6],6],[5,[4,3]]]],
[[2,[[4,7],5]],1],
[[8,7],[[[2,0],7],[1,[0,3]]]],
[[9,[[9,3],[9,5]]],[[8,7],[[4,1],[6,5]]]],
[[3,4],[[9,4],5]],
[[5,[[8,3],5]],1],
[[0,[[9,0],[3,2]]],[2,[7,[5,1]]]],
[[9,[[9,5],[8,6]]],[[4,4],[[3,8],[1,6]]]],
[[[1,[5,2]],9],[[4,6],[3,[8,0]]]],
[[1,7],[[1,7],9]],
[[[[3,4],3],[[7,5],[9,1]]],[[[5,0],[3,0]],[[7,9],6]]],
[[[7,2],[[1,0],[5,6]]],[[[3,7],[8,9]],6]],
[[[[1,1],1],[[8,6],[9,8]]],[[[1,8],4],[8,9]]],
[[[8,9],0],3],
[[[1,7],[1,[3,9]]],[6,[0,[8,5]]]],
[[0,5],[6,5]],
[[[[6,8],[4,5]],[[7,4],6]],[[3,6],5]],
[[8,[[0,9],8]],[9,[7,[7,9]]]],
[0,[[[7,1],2],[[0,4],4]]],
[[0,[[9,1],5]],[1,4]],
[3,4],
[[[9,3],[1,3]],[[[4,8],3],[[1,3],[9,0]]]],
[[[[5,1],7],[[9,2],8]],[[[6,8],[5,4]],[0,1]]],
[8,[[1,[3,0]],[[7,9],4]]],
[[[6,4],[[2,9],[9,0]]],[7,[[0,0],3]]],
[[3,[[9,6],6]],2],
[[5,[[3,1],[7,5]]],[[[6,7],9],[[4,6],[5,2]]]],
[[[4,[6,5]],8],[[6,[8,0]],[[9,3],3]]],
[[[[4,9],[2,8]],9],[[[5,0],0],[[3,4],[2,8]]]],
[[3,[7,1]],[9,[[1,8],7]]],
[[9,1],[0,[[0,7],[7,1]]]],
[[7,[0,[7,6]]],[[[5,3],1],[6,[4,5]]]],
[8,[[[2,1],[6,9]],[[3,3],[4,6]]]],
[0,[7,[3,0]]],
[[[[1,6],3],[5,[8,0]]],[[[6,6],7],1]],
[[[7,[8,3]],3],[[[2,8],5],[0,[9,5]]]],
[[[[5,1],4],[[1,2],1]],7],
[[[3,[7,5]],7],3],
[[9,[6,[1,1]]],[[[4,1],[2,2]],[[9,5],[7,7]]]],
[2,7],
[[[9,[8,6]],[[9,0],[6,5]]],[[[6,7],5],[[7,7],[2,3]]]],
[[[0,[6,4]],2],[4,[7,[7,5]]]],
[[[[6,1],[9,1]],[[6,1],9]],[[2,6],0]],
[[0,[[1,8],[3,5]]],[4,[[8,2],[4,2]]]],
[[[[9,3],[4,2]],2],[[[2,1],[7,1]],[4,8]]],
[[[3,[0,2]],3],8],
[[[4,[4,9]],9],[[[4,4],5],9]],
[[[[8,2],7],9],[[[1,0],[3,8]],[[7,7],0]]],
[[[3,2],[9,7]],[[9,[8,2]],[[5,5],3]]],
[[[7,[3,1]],[[8,3],1]],[[[8,6],[7,0]],4]],
[[9,[[9,1],5]],[[4,[1,1]],2]],
[[[[7,4],[0,3]],7],[8,[6,[3,3]]]],
[5,5],
[[6,7],[1,[7,[8,1]]]],
[[1,[0,4]],7],
[[[4,0],[[0,1],[2,2]]],[9,[[9,9],[3,0]]]],
[[[6,0],[[8,6],3]],[[5,1],[[8,1],[2,7]]]],
[[[[8,3],7],5],[9,[[5,1],8]]],
[[[[4,0],[5,2]],[[0,0],7]],2],
[[[[0,1],6],2],[[8,2],6]],
[[[[2,4],1],[[6,7],9]],[[[1,6],9],3]],
[[5,5],[[8,[7,7]],[5,8]]],
[[6,[[9,2],[9,7]]],[[[8,5],[4,4]],7]],
[[[9,[7,7]],[6,0]],[7,[[8,7],[1,2]]]],
[[7,[6,2]],[[9,[5,2]],[1,4]]],
[[[7,[5,9]],[[3,9],[4,5]]],[0,6]],
[[9,[8,[2,2]]],[[9,7],[1,1]]],
[[[[2,3],4],[[4,8],9]],[[9,[8,6]],[[0,9],0]]],
[[0,[[9,3],0]],[8,8]],
[[[[2,9],6],[[2,8],9]],[[[0,5],6],[[6,1],7]]],
[[9,[[8,3],[5,8]]],[[7,[3,0]],3]],
[[[4,[4,2]],0],1],
[[[[9,6],[5,8]],[6,2]],[[[8,0],[7,0]],[[5,6],4]]],
[[[8,0],[[4,3],[7,4]]],[[3,[7,9]],[[7,3],6]]],
[[3,[5,[0,3]]],[5,4]],
[[[[1,2],[6,3]],1],[[7,[5,2]],[[8,8],7]]],
[[4,[[8,0],[7,1]]],[[8,[8,0]],[[1,5],3]]]

]

m_v = 0
for l, r in itertools.permutations(inp, 2):
    l = copy.deepcopy(l)
    r = copy.deepcopy(r)

    v = [l, r]
    print(f"{l=} {r=}")
    do_add(v)
    m_v = max(do_mag(TreeZipper(v, [])), m_v)

print(m_v)
