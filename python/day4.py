from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Board:
    rows: list[list[int]]
    nums: set[int]
    foundnums: set[int]

    colcounts: list[int]
    rowcounts: list[int]
    invmap: dict[int, tuple[int, int]]
    won: bool

    @classmethod
    def parse(cls, s: str):
        rows = [
            [int(x) for x in row.strip().split()]
            for row in s.strip().splitlines()
        ]

        invmap = {}
        for y, row in enumerate(rows):
            for x, v in enumerate(row):
                invmap[v] = (x, y)

        nums = set(x for row in rows for x in row)
        colcounts = [0] * 5
        rowcounts = [0] * 5

        return cls(rows, nums, set(), colcounts, rowcounts, invmap, False)

    def check(self):
        return any(x == 5 for x in self.colcounts) or any(x == 5 for x in self.rowcounts)

    def add(self, n):
        if n not in self.nums:
            return False

        self.foundnums.add(n)

        col, row = self.invmap[n]
        self.colcounts[col] += 1
        self.rowcounts[row] += 1

        return self.check()


with open("day4.txt") as f:
    drawn = [int(i) for i in f.readline().strip().split(",")]
    boards = [Board.parse(x) for x in f.read().strip().split("\n\n")]

print(drawn)
print(boards)

def lol():
    for n in drawn:
        for board in boards:
            if board.won:
                continue
            won = board.add(n)
            if won:
                board.won = won
                unmarked = sum(board.nums - board.foundnums)
                score = unmarked * n
                print(n, score)

lol()
