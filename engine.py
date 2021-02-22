# -*- coding: utf-8 -*-

class GameState:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_column] = '--'
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        return self.get_possible_moves()

    def get_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][column][1]
                    if piece == 'P':
                        self.get_pawn_moves(row, column, moves)
                    elif piece == 'R':
                        self.get_rook_moves(row, column, moves)

    def get_pawn_moves(self, row, column, moves):
        ...

    def get_rook_moves(self, row, column, moves):
        ...


class Move:
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                              "5": 3, "6": 2, "7": 1, "8": 0}
        self.rows_to_ranks = {v: k for k, v in self.ranks_to_rows.items()}
        self.files_to_columns = {"a": 0, "b": 1, "c": 2, "d": 3,
                                 "e": 4, "f": 5, "g": 6, "h": 7}
        self.columns_to_files = {v: k for k, v in self.files_to_columns.items()}

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)

    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.rows_to_ranks[row]
