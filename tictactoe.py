#!/usr/bin/env python
from __future__ import print_function
import random


class Board(object):

    EMPTY_CELL = '.'

    def __init__(self, dim):
        self._dim = dim
        self._cells = list(Board.EMPTY_CELL * (dim ** 2))

    def __str__(self):
        rows = [''.join(self._cells[idx:idx + self._dim]) for idx in range(0, len(self._cells), self._dim)]
        return '\n'.join(rows) + '\n'

    @property
    def available_cells(self):
        return [idx for idx in range(len(self._cells)) if self._cells[idx] == Board.EMPTY_CELL]

    def is_empty(self):
        return len(self.available_cells) == len(self._cells)

    def is_full(self):
        return len(self.available_cells) == 0

    def is_cell_empty(self, idx):
        return self._cells[idx] == Board.EMPTY_CELL

    def get_cell(self, idx):
        return self._cells[idx]

    def set_cell(self, idx, val):
        self._cells[idx] = val


class Game(object):

    def __init__(self, player1_token, player2_token, dim):
        self._player1_token = player1_token
        self._player2_token = player2_token
        self._board = Board(dim)
        self._next_player = None
        self._winner = None

        # define win patterns for board
        self._win_patterns = []
        length = dim ** 2
        #   add horizontal patterns
        for row_idx in range(0, length, dim):
            self._win_patterns.append(range(row_idx, row_idx + dim))
        #   add vertical patterns
        for col_idx in range(0, dim):
            self._win_patterns.append(range(col_idx, length, dim))
        #   add diagonal patterns
        self._win_patterns.append(range(0, length, dim + 1))
        self._win_patterns.append(range(dim - 1, length - dim + 1, dim - 1))

        # define event handlers to be set by callers after construction
        self.on_player1_turn = None
        self.on_player2_turn = None
        self.on_game_update = None
        self.on_game_over = None

    def start(self):
        # ensure we're not already started
        if self._next_player is not None:
            raise RuntimeError('game already started')
        # ensure event handlers are set
        if self.on_player1_turn is None:
            raise RuntimeError('game needs an on_player1_turn event handler')
        if self.on_player2_turn is None:
            raise RuntimeError('game needs an on_player2_turn event handler')
        if self.on_game_update is None:
            raise RuntimeError('game needs an on_game_update event handler')
        if self.on_game_over is None:
            raise RuntimeError('game needs an on_game_over event handler')

        # run game loop
        self._next_player = 1
        while not self._is_game_over():
            self._next_turn()
            self.on_game_update(self._board)
        self.on_game_over(self._winner)

    def play_player1_turn(self, cell):
        if self._next_player is None:
            raise RuntimeError('game needs to be started first')
        self._board.set_cell(cell, self._player1_token)

    def play_player2_turn(self, cell):
        if self._next_player is None:
            raise RuntimeError('game needs to be started first')
        self._board.set_cell(cell, self._player2_token)

    def _check_winner(self):
        for pattern in self._win_patterns:
            items = [self._board.get_cell(i) for i in pattern]
            if all(item == self._player1_token for item in items): return self._player1_token
            if all(item == self._player2_token for item in items): return self._player2_token
        return None

    def _is_game_over(self):
        self._winner = self._check_winner()
        return self._winner is not None or self._board.is_full()

    def _next_turn(self):
        if self._next_player == 1:
            self.on_player1_turn(self._board.available_cells)
            self._next_player = 2
        else:
            self.on_player2_turn(self._board.available_cells)
            self._next_player = 1


if __name__ == '__main__':
    game = Game('x', 'o', 3)
    game.on_player1_turn = lambda available: game.play_player1_turn(random.choice(available))
    game.on_player2_turn = lambda available: game.play_player2_turn(random.choice(available))
    game.on_game_update = lambda board: print(board)
    game.on_game_over = lambda winner: print('{} wins'.format(winner) if winner else 'draw')
    game.start()
