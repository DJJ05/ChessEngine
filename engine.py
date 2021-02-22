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
        self.move_mapping = {
            'P': self.get_pawn_moves,
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
        }
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
                    self.move_mapping[piece](row, column, moves)
        return moves

    def get_pawn_moves(self, row, column, moves):
        if self.white_to_move:
            if row - 1 >= 0:
                if self.board[row-1][column] == '--':
                    moves.append(Move((row, column), (row - 1, column), self.board))
                    if row == 6 and self.board[row-2][column] == '--':
                        moves.append(Move((row, column), (row - 2, column), self.board))

                if column - 1 >= 0:
                    if self.board[row-1][column-1][0] == 'b':
                        moves.append(Move((row, column), (row - 1, column - 1), self.board))

                if column + 1 <= 7:
                    if self.board[row-1][column+1][0] == 'b':
                        moves.append(Move((row, column), (row - 1, column + 1), self.board))

        else:
            if len(self.board) > row + 1:
                if self.board[row+1][column] == '--':
                    moves.append(Move((row, column), (row + 1, column), self.board))
                    if row == 1 and self.board[row+2][column] == '--':
                        moves.append(Move((row, column), (row + 2, column), self.board))

                if column - 1 >= 0:
                    if self.board[row+1][column-1][0] == 'w':
                        moves.append(Move((row, column), (row + 1, column - 1), self.board))

                if column + 1 <= 7:
                    if self.board[row+1][column+1][0] == 'w':
                        moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def get_rook_moves(self, row, column, moves):
        ...

    def get_knight_moves(self, row, column, moves):
        ...

    def get_bishop_moves(self, row, column, moves):
        ...

    def get_queen_moves(self, row, column, moves):
        ...

    def get_king_moves(self, row, column, moves):
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
        self.move_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)

    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.rows_to_ranks[row]
