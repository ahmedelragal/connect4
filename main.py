import numpy as np
import random
import pygame
import sys
import math
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

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

winning_moves  = set()
def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece and ( (r,c) , (r , c+1 ) , (r , c+2) , (r , c+3) )  not in winning_moves:  
                winning_moves.add( tuple( ((r,c) , (r , c+1 ) , (r , c+2) , (r , c+3))   )  )
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece and ( (r,c) , (r+1 , c ) , (r+2 , c) , (r+3 , c)  )  not in winning_moves:
                winning_moves.add( tuple( ( (r,c) , (r+1 , c ) , (r+2 , c) , (r+3 , c) )  )  )

                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece and ( (r,c) , (r+1 , c+1 ) , (r+2 , c+2) , (r+3 , c+3) )   not in winning_moves:
                winning_moves.add( tuple( ( (r,c) , (r+1 , c+1 ) , (r+2 , c+2) , (r+3 , c+3) ) )  )

                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece  and  ( (r,c) , (r-1 , c+1 ) , (r-2 , c+2) , (r-3 , c+3)  )   not in winning_moves:
                winning_moves.add( tuple( ( (r,c) , (r-1 , c+1 ) , (r-2 , c+2) , (r-3 , c+3)  ) )  )
 
                return True


def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100000
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5000
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 200
	elif window.count(piece) == 2  and window.count(EMPTY) > 2:
			score += 10  # Encourage building connections

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4000
	if window.count(opp_piece) == 2 and window.count(EMPTY) == 2 :
		score -=  100
	elif window.count(opp_piece) == 2 and window.count(EMPTY) > 2:
		score -= 5  #

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return  len(get_valid_locations(board)) == 0
class Node (): 
	def __init__(self ,  state , children , utility_value , board = None , parent  = None):
		self.state  = state 
		self.children  = children  
		self.utility_value  = utility_value
		self.board = board
		self.parent = parent

		

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
# treetest= {0 : [Node ( 69 ,  None  , 0 ,  "7amada")] , 
# 	   1: [] , 
# 	   2 : [] , 
# 	   3: [] ,  
# 	   4:[] , 
# 	   5: []}



def minimax_with_pruning(board, depth, alpha, beta, maximizingPlayer, current_depth  , newnode ):
#   global root 

  valid_locations = get_valid_locations(board)
  is_terminal = is_terminal_node(board)

  if depth == 0 or is_terminal:
    # return Node(None, None, score_position(board, AI_PIECE), board)  # Leaf node
    return None  , score_position(board, AI_PIECE),

  if maximizingPlayer:
    value = -math.inf
    children = []
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, AI_PIECE)
      node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

      returned_node , val  = minimax(b_copy, depth - 1, alpha, beta, False, current_depth + 1 , node)
    #   print("1")
      node.utility_value = val
      newnode.children.append(node)
      children.append(node)
      value = max(value, val)
      alpha = max(alpha, value)
      if alpha >= beta:
         break
    # No need to set root.children here, children are appended within the loop

  else:  # Minimizing player
    value = math.inf
    children = []
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, PLAYER_PIECE)
      node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

      returned_node , val = minimax(b_copy, depth - 1, alpha, beta, True, current_depth + 1 , node)
    #   node = Node(col, returned_node.children, returned_node.utility_value, b_copy, parent=root if current_depth == 0 else root.children[current_depth - 1])  # Set parent based on current depth
      children.append(node)
      node.utility_value = val
      newnode.children.append(node)
      value = min(value, val)
      beta = min(beta, value)
      if alpha >= beta:
         break
    # No need to set root.children here, children are appended within the loop

  return newnode.state , newnode.utility_value





def minimax(board, depth,  maximizingPlayer, current_depth  , newnode ):
#   global root 

  valid_locations = get_valid_locations(board)
  is_terminal = is_terminal_node(board)

  if depth == 0 or is_terminal:
    # return Node(None, None, score_position(board, AI_PIECE), board)  # Leaf node
    return None  , score_position(board, AI_PIECE),

  if maximizingPlayer:
    value = -math.inf
    children = []
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, AI_PIECE)
      node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

      returned_node , val  = minimax(b_copy, depth - 1,  False, current_depth + 1 , node)
    #   print("1")
      node.utility_value = val
      newnode.children.append(node)
      children.append(node)
      value = max(value, val)

    # No need to set root.children here, children are appended within the loop

  else:  # Minimizing player
    value = math.inf
    children = []
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, PLAYER_PIECE)
      node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

      returned_node , val = minimax(b_copy, depth - 1,  True, current_depth + 1 , node)
    #   node = Node(col, returned_node.children, returned_node.utility_value, b_copy, parent=root if current_depth == 0 else root.children[current_depth - 1])  # Set parent based on current depth
      children.append(node)
      node.utility_value = val
      newnode.children.append(node)
      value = min(value, val)

    # No need to set root.children here, children are appended within the loop

  return newnode.state , newnode.utility_value

	


def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	# print(f"valid locations are {valid_locations}")
	return valid_locations



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

		col, value   = minimax(board,  6 , True , 0 , root)
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