# -*- coding: utf-8 -*-

import copy

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
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassant_possible = ()
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(
            self.current_castling_rights.white_king_side,
            self.current_castling_rights.black_king_side,
            self.current_castling_rights.white_queen_side,
            self.current_castling_rights.black_queen_side
        )]

    def make_move(self, move):
        self.board[move.start_row][move.start_column] = '--'
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move)

        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_column)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_column)

        self.white_to_move = not self.white_to_move

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_column] = move.piece_moved[0] + 'Q'

        if move.is_enpassant_move:
            self.board[move.start_row][move.end_column] = '--'

        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_column)
        else:
            self.enpassant_possible = ()

        if move.is_castle_move:
            if move.end_column - move.start_column == 2:
                self.board[move.end_row][move.end_column - 1] = self.board[move.end_row][move.end_column + 1]
                self.board[move.end_row][move.end_column + 1] = '--'

            else:
                self.board[move.end_row][move.end_column + 1] = self.board[move.end_row][move.end_column - 2]
                self.board[move.end_row][move.end_column - 2] = '--'

        self.update_castle_rights(move)
        self.castle_rights_log.append(
            CastleRights(
                self.current_castling_rights.white_king_side,
                self.current_castling_rights.black_king_side,
                self.current_castling_rights.white_queen_side,
                self.current_castling_rights.black_queen_side
            )
        )

    def update_castle_rights(self, move):
        if move.piece_moved == 'wK':
            self.current_castling_rights.white_king_side = False
            self.current_castling_rights.white_queen_side = False

        elif move.piece_moved == 'bK':
            self.current_castling_rights.black_king_side = False
            self.current_castling_rights.black_queen_side = False

        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_column == 0:
                    self.current_castling_rights.white_queen_side = False
                elif move.start_column == 7:
                    self.current_castling_rights.white_king_side = False

        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_column == 0:
                    self.current_castling_rights.black_queen_side = False
                elif move.start_column == 7:
                    self.current_castling_rights.black_king_side = False

        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_column == 0:
                    self.current_castling_rights.wqs = False
                elif move.end_column == 7:
                    self.current_castling_rights.wks = False

        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_column == 0:
                    self.current_castling_rights.bqs = False
                elif move.end_column == 7:
                    self.current_castling_rights.bks = False

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured

            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_column)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_column)

            if move.is_enpassant_move:
                self.board[move.end_row][move.end_column] = '--'
                self.board[move.start_row][move.end_column] = move.piece_captured
                self.enpassant_possible = (move.end_row, move.end_column)

            if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ()

            self.castle_rights_log.pop()
            self.current_castling_rights = copy.deepcopy(self.castle_rights_log[-1])

            if move.is_castle_move:
                if move.end_column - move.start_column == 2:
                    self.board[move.end_row][move.end_column + 1] = self.board[move.end_row][move.end_column - 1]
                    self.board[move.end_row][move.end_column - 1] = '--'

                else:
                    self.board[move.end_row][move.end_column - 2] = self.board[move.end_row][move.end_column + 1]
                    self.board[move.end_row][move.end_column + 1] = '--'

            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        temp_enpassant_possible = self.enpassant_possible
        temp_castle_rights = CastleRights(
            self.current_castling_rights.white_king_side,
            self.current_castling_rights.black_king_side,
            self.current_castling_rights.white_queen_side,
            self.current_castling_rights.black_queen_side
        )
        moves = self.get_possible_moves()

        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        for move in moves[::-1]:
            self.make_move(move)
            self.white_to_move = not self.white_to_move

            if self.in_check():
                moves.remove(move)

            self.white_to_move = not self.white_to_move
            self.undo_move()

        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.stalemate = False
            self.checkmate = False

        self.enpassant_possible = temp_enpassant_possible
        self.current_castling_rights = temp_castle_rights
        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, row, column):
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move.end_row == row and move.end_column == column:
                return True
        return False

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
                if self.board[row - 1][column] == '--':
                    moves.append(Move((row, column), (row - 1, column), self.board))
                    if row == 6 and self.board[row - 2][column] == '--':
                        moves.append(Move((row, column), (row - 2, column), self.board))

                if column - 1 >= 0:
                    if self.board[row - 1][column - 1][0] == 'b':
                        moves.append(Move((row, column), (row - 1, column - 1), self.board))
                    elif (row - 1, column - 1) == self.enpassant_possible:
                        moves.append(Move((row, column), (row - 1, column - 1), self.board, is_enpassant_move=True))

                if column + 1 <= 7:
                    if self.board[row - 1][column + 1][0] == 'b':
                        moves.append(Move((row, column), (row - 1, column + 1), self.board))
                    elif (row - 1, column + 1) == self.enpassant_possible:
                        moves.append(Move((row, column), (row - 1, column + 1), self.board, is_enpassant_move=True))

        else:
            if len(self.board) > row + 1:
                if self.board[row + 1][column] == '--':
                    moves.append(Move((row, column), (row + 1, column), self.board))
                    if row == 1 and self.board[row + 2][column] == '--':
                        moves.append(Move((row, column), (row + 2, column), self.board))

                if column - 1 >= 0:
                    if self.board[row + 1][column - 1][0] == 'w':
                        moves.append(Move((row, column), (row + 1, column - 1), self.board))
                    elif (row + 1, column - 1) == self.enpassant_possible:
                        moves.append(Move((row, column), (row + 1, column - 1), self.board, is_enpassant_move=True))

                if column + 1 <= 7:
                    if self.board[row + 1][column + 1][0] == 'w':
                        moves.append(Move((row, column), (row + 1, column + 1), self.board))
                    elif (row + 1, column + 1) == self.enpassant_possible:
                        moves.append(Move((row, column), (row + 1, column + 1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, row, column, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.white_to_move else 'w'

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_column = column + direction[1] * i

                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]

                    if end_piece == '--':
                        moves.append(Move((row, column), (end_row, end_column), self.board))

                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break

                    else:
                        break

                else:
                    break

    def get_knight_moves(self, row, column, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_to_move else 'b'

        for move in knight_moves:
            end_row = row + move[0]
            end_column = column + move[1]

            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]

                if end_piece[0] != ally_color:
                    moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_bishop_moves(self, row, column, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_to_move else 'w'

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_column = column + direction[1] * i

                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]

                    if end_piece == '--':
                        moves.append(Move((row, column), (end_row, end_column), self.board))

                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break

                    else:
                        break

                else:
                    break

    def get_queen_moves(self, row, column, moves):
        self.get_rook_moves(row, column, moves)
        self.get_bishop_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = 'w' if self.white_to_move else 'b'

        for i in range(8):
            end_row = row + king_moves[i][0]
            end_column = column + king_moves[i][1]

            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]

                if end_piece[0] != ally_color:
                    moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_castle_moves(self, row, column, moves):
        if self.square_under_attack(row, column):
            return

        if (self.white_to_move and self.current_castling_rights.white_king_side) or (not self.white_to_move and self.current_castling_rights.black_king_side):
            self.get_kingside_castle_moves(row, column, moves)

        if (self.white_to_move and self.current_castling_rights.white_queen_side) or (not self.white_to_move and self.current_castling_rights.black_queen_side):
            self.get_queenside_castle_moves(row, column, moves)

    def get_kingside_castle_moves(self, row, column, moves):
        if self.board[row][column + 1] == '--' and self.board[row][column + 2] == '--':
            if not self.square_under_attack(row, column+1) and not self.square_under_attack(row, column+2):
                moves.append(Move((row, column), (row, column+2), self.board, is_castle_move=True))

    def get_queenside_castle_moves(self, row, column, moves):
        if self.board[row][column - 1] == '--' and self.board[row][column - 2] == '--' and self.board[row][column -3] == '--':
            if not self.square_under_attack(row, column-1) and not self.square_under_attack(row, column-2):
                moves.append(Move((row, column), (row, column-2), self.board, is_castle_move=True))


class CastleRights():
    def __init__(self, white_king_side, black_king_side, white_queen_side, black_queen_side):
        self.white_king_side = white_king_side
        self.black_king_side = black_king_side
        self.white_queen_side = white_queen_side
        self.black_queen_side = black_queen_side


class Move:
    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
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

        self.is_pawn_promotion = False
        self.is_enpassant_move = is_enpassant_move
        self.is_castle_move = is_castle_move

        if self.is_enpassant_move:
            self.piece_captured = 'wP' if self.piece_moved == 'bP' else 'bP'

        if (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7):
            self.is_pawn_promotion = True

        self.move_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)

    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.rows_to_ranks[row]
