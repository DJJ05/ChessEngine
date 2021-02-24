# -*- coding: utf-8 -*-

import pygame
import engine

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

        if move_made:
            valid_moves = game_state.get_valid_moves()

            if game_state.in_check() and not game_state.checkmate and game_state.square_under_attack(game_state.white_king_location[0], game_state.white_king_location[1]):
                print('White is now in check.')
            elif game_state.in_check() and not game_state.checkmate:
                print('Black is now in check.')
            elif game_state.checkmate and game_state.square_under_attack(game_state.white_king_location[0], game_state.white_king_location[1]):
                print('White has been checkmated. Black wins.')
            elif game_state.checkmate:
                print('Black has been checkmated. White wins.')
            elif game_state.stalemate:
                print('The game has been stalemated and it is drawn.')

            move_made = False

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main()
