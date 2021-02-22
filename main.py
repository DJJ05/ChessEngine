# -*- coding: utf-8 -*-

import pygame
import engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (SQ_SIZE, SQ_SIZE))


def draw_board(screen):
    colors = [pygame.Color('white'), (119, 148, 85)]

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row+column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state.board)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False
    undo_loop = False
    load_images()
    running = True
    selected_square = ()
    player_clicks = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                column = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                piece = game_state.board[row][column]

                if (len(player_clicks) == 0) and ((piece == '--' or piece[0] == 'w' and not game_state.white_to_move) or (piece[0] == 'b' and game_state.white_to_move)):
                    ...

                elif selected_square == (row, column):
                    selected_square = ()
                    player_clicks = []

                else:
                    selected_square = (row, column)
                    player_clicks.append(selected_square)

                if len(player_clicks) == 2:
                    move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                    if move in valid_moves:
                        print(move.get_chess_notation())
                        game_state.make_move(move)
                        move_made = True
                        selected_square = ()
                        player_clicks = []
                    else:
                        player_clicks = [selected_square]

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    undo_loop = False
                    move_made = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    undo_loop = True
                    move_made = True

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        if undo_loop:
            game_state.undo_move()

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main()
