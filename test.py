import numpy as np
import random
import pygame
import sys
import os
import math
from engine import *

score = [0, 0]  # Score for red and yellow players

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
# height = (ROW_COUNT * SQUARESIZE) + SQUARESIZE * 2
size = (width, height + 200)
screen = pygame.display.set_mode(size)
RADIUS = int(SQUARESIZE/2 - 5)


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    draw_button()
    display_score()
    pygame.display.update()
     
     
    
def draw_button():
    # Draw the button rectangle
    pygame.draw.rect(screen, YELLOW, (0, height + SQUARESIZE//2, width//2, SQUARESIZE))
    # Draw the button text
    font = pygame.font.Font(None, 36)
    text = font.render("Click Me", True, WHITE)
    text_rect = text.get_rect(center=(width/2, height+SQUARESIZE/2))
    screen.blit(text, text_rect)

def display_score():
    # Draw the score text
    font = pygame.font.Font(None, 36)
    text = font.render("Score: 0", True, WHITE)  # Replace 0 with actual score value
    text_rect = text.get_rect(midtop=(width/2, height+SQUARESIZE-10))
    screen.blit(text, text_rect)






# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Font
FONT = pygame.font.SysFont(None, 30)

# Function to display text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function to display menu
def display_menu(screen, algorithm, difficulty):
    screen.fill(WHITE)
    draw_text("Connect 4 Game", FONT, BLACK, screen, 200, 50)
    draw_text("Algorithm:", FONT, BLACK, screen, 50, 100)
    draw_text(algorithm, FONT, BLACK, screen, 200, 100)
    draw_text("Difficulty:", FONT, BLACK, screen, 50, 150)
    draw_text(str(difficulty), FONT, BLACK, screen, 200, 150)

# Main function
def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4 Menu")

    algorithm = "Minimax without pruning"
    difficulty = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if algorithm == "Minimax without pruning":
                        algorithm = "Minimax with pruning"
                    else:
                        algorithm = "Minimax without pruning"
                elif event.key == pygame.K_RIGHT:
                    if difficulty < 10:
                        difficulty += 1
                elif event.key == pygame.K_LEFT:
                    if difficulty > 1:
                        difficulty -= 1
                elif event.key == pygame.K_RETURN:
                    running = False

        display_menu(screen, algorithm, difficulty)
        pygame.display.flip()

    print("Algorithm:", algorithm)
    print("Difficulty:", difficulty)
    
    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()
    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    # turn = random.randint(PLAYER, AI)
    turn  = PLAYER
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            score[PLAYER] += 1
                            print(score)

                        turn += 1
                        turn = turn % 2

                        draw_board(board)

        # # Ask for Player 2 Input
        if turn == AI and not game_over:				

            root = Node(None, [], 0 , board= board)
            # Traversing the children  
            if algorithm == "Minimax without pruning":
                print(difficulty)
                col, value   = minimax(board,  difficulty , True , 0 , root)
                
            else:
                 #modify later -------------------------------------------
                 print("pruniing")
                 col, value   = minimax(board,  difficulty , True , 0 , root)
                 
            print(root.board) 
            for child in root.children :
                print("***********************************level 1****************************************") 
                print(child.board) 
                for c  in child.children : 
                    print
                    print(c.board)
                    print("***********************************level 2****************************************") 

                    for  x in c.children : 
                        print (x.board)

            col = 0 
            max_val =  - math.inf
            for child in root.children :
                # print( child.state)
                if child.utility_value > max_val : 
                    max_val = child.utility_value 
                    col  = child.state

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    score[AI] +=1 
                    print(score)

                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000) # This line is added after the 2 last print functions


if __name__ == "__main__":
    main()

