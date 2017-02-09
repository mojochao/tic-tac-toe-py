#!/usr/bin/env python
from __future__ import print_function
import random


def contains_only(seq, val):
    for item in seq:
        if item != val:
            return False
    return True


class Board(object):

    EMPTY_CELL = '.'

    def __init__(self, dim):
        self.dim = dim
        self.cells = list(Board.EMPTY_CELL * (dim ** 2))

    def __str__(self):
        rows = [''.join(self.cells[i:i + self.dim]) for i in range(0, len(self.cells), self.dim)]
        return '\n'.join(rows) + '\n'

    def is_empty(self):
        return len(self.available_cells) == len(self.cells)

    def is_full(self):
        return len(self.available_cells) == 0

    @property
    def available_cells(self):
        return [i for i in range(len(self.cells)) if self.cells[i] == Board.EMPTY_CELL]

    def is_cell_available(self, i):
        return self.cells[i] == Board.EMPTY_CELL

    def get_cell(self, i):
        return self.cells[i]

    def set_cell(self, i, val):
        self.cells[i] = val

    @property
    def win_patterns(self):
        lines = []
        length = self.dim ** 2
        # add horizontals
        for row_idx in range(0, length, self.dim):
            lines.append(range(row_idx, row_idx + self.dim))
        # add verticals
        for col_idx in range(0, self.dim):
            lines.append(range(col_idx, length, self.dim))
        # add diagonals
        lines.append(range(0, length, self.dim + 1))
        lines.append(range(self.dim - 1, length - self.dim + 1, self.dim - 1))
        # return result
        return lines


class Game(object):

    def __init__(self, player1_token, player2_token, dim):
        self.player1_token = player1_token
        self.player2_token = player2_token
        self.board = Board(dim)
        self.next_player = None
        self.winner = None
        self.on_player1_turn = None
        self.on_player2_turn = None
        self.on_game_update = None
        self.on_game_over = None

    def start(self):
        self.next_player = 1
        while not self._is_game_over():
            self._next_turn()
            self.on_game_update(self.board)
        self.on_game_over(self.winner)

    def play_player1_turn(self, cell):
        self._play_turn(cell, self.player1_token)

    def play_player2_turn(self, cell):
        self._play_turn(cell, self.player2_token)

    def _check_winner(self):
        for pattern in self.board.win_patterns:
            line = map(lambda i: self.board.cells[i], pattern)
            if contains_only(line, self.player1_token):
                return self.player1_token
            if contains_only(line, self.player2_token):
                return self.player2_token
        return None

    def _is_game_over(self):
        self.winner = self._check_winner()
        return self.winner is not None or self.board.is_full()

    def _next_turn(self):
        if self.next_player == 1:
            self.on_player1_turn(self.board.available_cells)
            self.next_player = 2
        else:
            self.on_player2_turn(self.board.available_cells)
            self.next_player = 1

    def _play_turn(self, cell, token):
        if self.next_player is None:
            raise RuntimeError('game not started')
        if not self.board.is_cell_available(cell):
            raise RuntimeError('cell {} not available'.format(cell))
        self.board.set_cell(cell, token)


if __name__ == '__main__':
    game = Game('x', 'o', 3)
    game.on_player1_turn = lambda available: game.play_player1_turn(random.choice(available))
    game.on_player2_turn = lambda available: game.play_player2_turn(random.choice(available))
    game.on_game_update = lambda board: print(board)
    game.on_game_over = lambda winner: print('{} wins'.format(winner) if winner else 'draw')
    game.start()
