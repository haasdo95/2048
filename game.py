import torch
from random import random, randint
from enum import Enum
class Move(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class TwoK:
    def __init__(self):
        self.grid = torch.zeros(4, 4)
        self.insert_rand()
        self.insert_rand()

    def insert_rand(self):
        num_inserted = 1 if random() < 0.5 else 2
        indices = (self.grid == 0).nonzero()
        num_zeros = indices.size()[0]
        index = indices[randint(0, num_zeros - 1)]
        self.grid[index[0]][index[1]] = num_inserted

    def _collapse_column(self, column, is_up):
        prev_elem = 0
        curr_index = 0 if is_up else 3
        step = 1 if is_up else -1
        column_iter = column
        if not is_up:
            column_iter = reversed(list(column))
        for elem in column_iter:
            if elem != 0:
                if prev_elem == elem: # time to collapse!
                    prev_elem = 0
                    column[curr_index - step] = elem + 1
                else:
                    prev_elem = elem
                    column[curr_index] = elem
                    curr_index += step
        # zero out stuff
        if is_up:
            for row in range(curr_index, 4):
                column[row] = 0
        else:
            for row in range(curr_index + 1):
                column[row] = 0

    def _move_up(self):
        for col in range(4):
            column = self.grid[:, col]
            self._collapse_column(column, True)

    def _move_down(self):
        for col in range(4):
            column = self.grid[:, col]
            self._collapse_column(column, False)

    # any zero slot OR two adjacent the same
    def _column_can_move(self, column):
        prev_elem = 0
        for elem in column:
            if elem == 0:
                return True
            if elem == prev_elem:
                return True
            prev_elem = elem
        return False

    def _can_move(self):
        for col in range(4):
            column = self.grid[:, col]
            if self._column_can_move(column):
                return True
        return False

    def can_move(self, move: Move):
        if move == Move.UP or move == Move.DOWN:
            return self._can_move()
        self.grid = torch.t(self.grid)
        can_move = self._can_move()
        self.grid = torch.t(self.grid)
        return can_move

    def move(self, move: Move):
        if move == Move.UP:
            self._move_up()
        elif move == Move.DOWN:
            self._move_down()
        else:
            self.grid = torch.t(self.grid)
            if move == Move.LEFT:
                self._move_up()
            else:
                self._move_down()
            self.grid = torch.t(self.grid)

if __name__ == '__main__':
    tk = TwoK()
    while True:
        print(tk.grid)
        inp = input()
        if inp == "w":
            tk.move(Move.UP)
        elif inp == "a":
            tk.move(Move.LEFT)
        elif inp == "s":
            tk.move(Move.DOWN)
        elif inp == "d":
            tk.move(Move.RIGHT)
        else:
            raise ValueError
        tk.insert_rand()
