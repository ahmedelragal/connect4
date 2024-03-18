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
	pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

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
			#print(event.pos)
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

					# print_board(board)
					draw_board(board)


	# # Ask for Player 2 Input
	if turn == AI and not game_over:				

		root = Node(None, [], 0 , board= board)
		# Traversing the children  

		col, value   = minimax(board,  3 , True , 0 , root)
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
			#pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				score[AI] +=1 
				print(score)
				# label = myfont.render("Player 2 wins!!", 1, YELLOW)
				# screen.blit(label, (40,10))
				# game_over = True

			print_board(board)
			draw_board(board)


			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)