from __future__ import annotations
import functools
import dataclasses
from typing import Any, Optional

from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    left_one: Optional[str]
    left_two: Optional[str]
    right_one: Optional[str]
    right_two: Optional[str]

    one: tuple[Optional[str], Optional[str], Optional[str], Optional[str]]
    two: tuple[Optional[str], Optional[str], Optional[str], Optional[str]]
    three: tuple[Optional[str], Optional[str], Optional[str], Optional[str]]
    four: tuple[Optional[str], Optional[str], Optional[str], Optional[str]]

    one_two: Optional[str]
    two_three: Optional[str]
    three_four: Optional[str]


solved_state = State(
    left_one=None,
    left_two=None,
    right_one=None,
    right_two=None,
    one=("a", "a", "a", "a"),
    two=("b", "b", "b", "b"),
    three=("c", "c", "c", "c"),
    four=("d", "d", "d", "d"),
    one_two=None,
    two_three=None,
    three_four=None,
)


def solved(state: State) -> bool:
    return state == solved_state


def init_state() -> State:
    return State(
        left_one=None,
        left_two=None,
        right_one=None,
        right_two=None,
        one=("d", "d", "d", "a"),
        two=("d", "b", "c", "c"),
        three=("a", "a", "b", "b"),
        four=("c", "c", "a", "b"),
        one_two=None,
        two_three=None,
        three_four=None,
    )


def target_column_for(s: str) -> str:
    return {"a": "one", "b": "two", "c": "three", "d": "four"}[s]

def target_vale_for(s: str) -> str:
    return {"one": "a", "two": "b", "three": "c", "four": "d"}[s]


def topmost_in_column(c: Column) -> Optional[str]:
    next((x for x in c[::-1] if x is not None), None)


def target_column_for_opt(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    return target_column_for(s)


def none_to_list(n: Optional[str]) -> list[str]:
    if n is None:
        return []
    return [n]


def verify_move(state: State, from_: str, to: str) -> bool:
    if to == "left_one":
        return state.left_one is None
    elif to == "left_two":
        return state.left_two is None
    elif to == "right_one":
        return state.right_one is None
    elif to == "right_two":
        return state.right_two is None
    elif to == "one":
        return all(v is None or v == "a" for v in state.one)
    elif to == "two":
        return all(v is None or v == "b" for v in state.two)
    elif to == "three":
        return all(v is None or v == "c" for v in state.three)
    elif to == "four":
        return all(v is None or v == "d" for v in state.four)
    elif to == "one_two":
        return state.one_two is None
    elif to == "two_three":
        return state.two_three is None
    elif to == "three_four":
        return state.three_four is None
    raise Exception("no")


def check_crossings(state: State, from_: str, to: str) -> bool:
    opposite_sides = {
        "left_two": {"left_one"},
        "one_two": {"left_one", "left_two", "one"},
        "two_three": {"left_one", "left_two", "one", "two", "one_two"},
        "three_four": {
            "left_one",
            "left_two",
            "one",
            "two",
            "three",
            "one_two",
            "two_three",
        },
        "right_two": {
            "left_one",
            "left_two",
            "one",
            "two",
            "three",
            "four",
            "one_two",
            "two_three",
            "three_four",
        },
    }

    for k, v in opposite_sides.items():
        if k == from_:
            continue
        if getattr(state, k) and (
            (from_ in v and to not in v) or (to in v and from_ not in v)
        ):
            return False

    return True


def targets_from_position(state: State, pos: str):
    moves = {
        "left_one": none_to_list(target_column_for_opt(state.left_one)),
        "left_two": none_to_list(target_column_for_opt(state.left_two)),
        "right_one": none_to_list(target_column_for_opt(state.right_one)),
        "right_two": none_to_list(target_column_for_opt(state.right_two)),
        "one": [
            "left_one",
            "left_two",
            "right_one",
            "right_two",
            "one_two",
            "two_three",
            "three_four",
        ]
        + none_to_list(target_column_for_opt(topmost_in_column(state.one))),
        "two": [
            "left_one",
            "left_two",
            "right_one",
            "right_two",
            "one_two",
            "two_three",
            "three_four",
        ]
        + none_to_list(target_column_for_opt(topmost_in_column(state.two))),
        "three": [
            "left_one",
            "left_two",
            "right_one",
            "right_two",
            "one_two",
            "two_three",
            "three_four",
        ]
        + none_to_list(target_column_for_opt(topmost_in_column(state.three))),
        "four": [
            "left_one",
            "left_two",
            "right_one",
            "right_two",
            "one_two",
            "two_three",
            "three_four",
        ]
        + none_to_list(target_column_for_opt(topmost_in_column(state.four))),
        "one_two": none_to_list(target_column_for_opt(state.one_two)),
        "two_three": none_to_list(target_column_for_opt(state.two_three)),
        "three_four": none_to_list(target_column_for_opt(state.three_four)),
    }[pos]

    p_moves = [
        x
        for x in moves
        if x != pos and verify_move(state, pos, x) and check_crossings(state, pos, x)
    ]

    for v in ["one", "two", "three", "four"]:
        if v in p_moves:
            return [v]
    return p_moves


def depth_to(state: State, pos) -> int:
    c = getattr(state, pos)
    if not isinstance(c, tuple):
        return 0

    for i, v in enumerate(c):
        if v is None:
            return len(c) - (i + 1)

    return 0


def depth_from(state: State, pos) -> int:
    c = getattr(state, pos)
    if not isinstance(c, tuple):
        return 0

    for i, v in enumerate(c[::-1]):
        if v is not None:
            return i

    return 0


import networkx as nx

cost_map = nx.Graph(
    [
        ("left_one", "left_two"),
        ("left_two", 0),
        (0, "one"),
        (0, "one_two"),
        ("one_two", 1),
        (1, "two"),
        (1, "two_three"),
        ("two_three", 2),
        (2, "three"),
        (2, "three_four"),
        ("three_four", 3),
        (3, "four"),
        (3, "right_two"),
        ("right_two", "right_one"),
    ]
)


cost_multiplier = {"a": 1, "b": 10, "c": 100, "d": 1000}


def column_satisfied(state: State, pos: str) -> bool:
    if pos == "one":
        return all(x is None or x == "a" for x in state.one)
    elif pos == "two":
        return all(x is None or x == "b" for x in state.two)
    elif pos == "three":
        return all(x is None or x == "c" for x in state.three)
    elif pos == "four":
        return all(x is None or x == "d" for x in state.four)
    return False


def thing_at_position(state: State, pos: str) -> Optional[str]:
    x = getattr(state, pos)
    if x is None or isinstance(x, str):
        return x
    return next((v for v in x[::-1] if v is not None), None)


def steps_in_move(state: State, from_: str, to: str) -> int:
    from_depth = depth_from(state, from_)
    to_depth = depth_to(state, to)
    return nx.shortest_path_length(cost_map, from_, to) + from_depth + to_depth


def apply_move(state: State, from_: str, to: str) -> State:
    thing = thing_at_position(state, from_)
    x = getattr(state, from_)
    if isinstance(x, str):
        state = dataclasses.replace(state, **{from_: None})
    else:
        x = list(x)
        for i in range(len(x) - 1, -1, -1):
            if x[i] is not None:
                x[i] = None
                break
        state = dataclasses.replace(state, **{from_: tuple(x)})

    x = getattr(state, to)
    if x is None:
        state = dataclasses.replace(state, **{to: thing})
    else:
        x = list(x)
        for i in range(len(x)):
            if x[i] is None:
                x[i] = thing
                break
        state = dataclasses.replace(state, **{to: tuple(x)})

    return state


# desired_depth_logs = {
#     (0, 'three', 'one_two'),
#     (1, 'two', 'three'),
#     (2, 'two', 'two_three'),
#     (3, 'one_two', 'two'),
#     (4, 'one', 'two'),
#     (5, 'four', 'three_four'),
#     (6, 'four', 'right_two'),
#     (7, 'three_four', 'four'),
#     (8, 'two_three', 'four'),
#     (9, 'right_two', 'one')
# }

# desired_depth_logs = {
#     (i, *v)
#     for i, v in enumerate(
#         [
#             ("one", "left_two"),
#             ("three", "one_two"),
#             ("two", "two_three"),
#             ("three", "right_one"),
#             ("two_three", "three"),
#             ("two", "two_three"),
#             ("one_two", "two"),
#             ("one", "one_two"),
#             ("left_two", "one"),
#             ("four", "right_two"),
#             ("four", "three_four"),
#             ("three_four", "three"),
#             ("two_three", "four"),
#             ("one_two", "four"),
#             ("right_two", "two"),
#             ("right_one", "one"),
#         ]
#     )
# }

possible_positions = [
    "left_one",
    "left_two",
    "right_one",
    "right_two",
    "one",
    "two",
    "three",
    "four",
    "one_two",
    "two_three",
    "three_four",
]


@functools.lru_cache(maxsize=1000)
def find_min_moves(state: State):#, depth: int, c: bool):
    if solved(state):
        return 0, [], True
    # if depth > 15:
    #     return 0, [], False
    minimum = None
    move = []
    terminates = False
    for start in possible_positions:
        thing = thing_at_position(state, start)
        if thing is None:
            continue
        if column_satisfied(state, start):
            continue
        targets = targets_from_position(state, start)
        for target in targets:
            # c_n = c and (depth, start, target) in desired_depth_logs
            # if c_n:
            #     cost = steps_in_move(state, start, target) * cost_multiplier[thing]
            #     print(depth, state)
            #     print(f"{depth} {start} ({thing}) -> {target}, cost={cost}")
            # else:
            #     pass
            #     # continue
            next_costs, next_steps, this_terminates = find_min_moves(
                apply_move(state, start, target)#, depth + 1, c_n
            )

            if not this_terminates:
                continue
            cost = (
                steps_in_move(state, start, target) * cost_multiplier[thing]
                + next_costs
            )
            # print(cost)
            if minimum is None or cost < minimum:
                minimum = cost
                move = [(start, target), *next_steps]
                terminates = True
    return minimum or 0, move, terminates


if __name__ == "__main__":
    print(find_min_moves(init_state()))#, 0, True))
