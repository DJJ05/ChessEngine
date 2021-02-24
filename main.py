# -*- coding: utf-8 -*-

import pygame
import engine
import math

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
LOG_MOVES = True
IMAGES = {}


def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (SQ_SIZE, SQ_SIZE))


def draw_board(screen):
    global colors
    colors = [pygame.Color('white'), (119, 148, 85)]

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_squares(screen, game_state, valid_moves, selected_square):
    if selected_square != ():
        row, column = selected_square

        if game_state.board[row][column][0] == ('w' if game_state.white_to_move else 'b'):
            shape = pygame.Surface((SQ_SIZE, SQ_SIZE))
            shape.set_alpha(100)
            shape.fill(pygame.Color('blue'))
            screen.blit(shape, (column * SQ_SIZE, row * SQ_SIZE))

            for move in valid_moves:
                if move.start_row == row and move.start_column == column:
                    if game_state.board[move.end_row][move.end_column] != '--':
                        shape.fill(pygame.Color('red'))
                        screen.blit(shape, (move.end_column * SQ_SIZE, move.end_row * SQ_SIZE))
                    else:
                        shape.fill(pygame.Color('yellow'))
                        screen.blit(shape, (move.end_column * SQ_SIZE, move.end_row * SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, selected_square):
    draw_board(screen)
    highlight_squares(screen, game_state, valid_moves, selected_square)
    draw_pieces(screen, game_state.board)


def animate_move(move, screen, board, clock):
    global colors
    delta_row = move.end_row - move.start_row
    delta_column = move.end_column - move.start_column
    frames_per_square = round(math.sqrt(abs(delta_row) ** 2 + abs(delta_column) ** 2))
    frames_per_square = (frames_per_square + (round(DIMENSION / 2) - frames_per_square) * 2) if (frames_per_square + (round(DIMENSION / 2) - frames_per_square) * 2) > 0 else 1
    frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square

    for frame in range(frame_count + 1):
        row, column = (move.start_row + delta_row * frame / frame_count, move.start_column + delta_column * frame / frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        color = colors[(move.end_row + move.end_column) % 2]
        end_square = pygame.Rect(move.end_column * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, end_square)

        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)

        screen.blit(IMAGES[move.piece_moved], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    screen.fill(pygame.Color('white'))

    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False
    load_images()
    running = True
    selected_square = ()
    player_clicks = []
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()
                    column = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    piece = game_state.board[row][column]

                    if (len(player_clicks) == 0) and (
                            (piece == '--' or piece[0] == 'w' and not game_state.white_to_move) or (
                            piece[0] == 'b' and game_state.white_to_move)):
                        ...

                    elif selected_square == (row, column):
                        selected_square = ()
                        player_clicks = []

                    else:
                        selected_square = (row, column)
                        player_clicks.append(selected_square)

                    if len(player_clicks) == 2:
                        move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)

                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                if LOG_MOVES:
                                    print(f'MOVED: {move.get_chess_notation()}')

                                game_state.make_move(valid_moves[i])
                                move_made = True
                                selected_square = ()
                                player_clicks = []

                        if not move_made:
                            player_clicks = [selected_square]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game_state.undo_move()
                    valid_moves = game_state.get_valid_moves()
                    move_made = False

                elif event.key == pygame.K_s:
                    pygame.image.save(screen, 'capture.jpeg')
                    print('Captured screen.')

                elif event.key == pygame.K_r:
                    game_state = engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    selected_square = ()
                    player_clicks = []
                    move_made = False

        if move_made:
            if not game_state.move_log[-1].is_enpassant_move and not game_state.move_log[-1].is_castle_move:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)

            valid_moves = game_state.get_valid_moves()

            if game_state.checkmate:
                game_over = True
                if game_state.white_to_move:
                    print('Black wins by checkmate')
                else:
                    print('White wins by checkmate')

            elif game_state.stalemate:
                game_over = True
                print('Stalemate')

            move_made = False

        draw_game_state(screen, game_state, valid_moves, selected_square)
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main()
