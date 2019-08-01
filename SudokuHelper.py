# *************************************************************************
#  File   : SudokuHelper.py
#  Author : Tanmay 
# *************************************************************************

# fetch input puzzle file to solve
def getTestFile():
	try: 
		init_values = input("Enter no. of initial values (1-71): ")
		if (int(init_values) > 0 and int(init_values) < 72): 
			test = input("Enter test file (1-10): ")
			if(int(test) > 0 and int(test) < 11):
				filename = "sudoku_problems/" + init_values + "/" + test + ".sd"
			else:
				print("Invalid input: test file no. must be between 1 & 10")
				exit()
		else:
			print("Invalid input: no. of initial values must be between 1 & 71")
			exit()
	except:
		print("file <%s> not found" % filename)
		exit()

	return filename

def createBoard(filename):
	data = open(filename).read().split('\n')

	board = []

	for r in range(0,9):
		row = data[r].split()
		for col in range(0,9):
			row[col] = int(row[col])
		board.append(row)
			
	return board

def printBoard(board):  
	for row in range(0,9):
		if row in [3,6]:
			print("-----+-----+-----")
			print(str(board[row][0]) + " " + str(board[row][1]) + " " + str(board[row][2]) + "|" +
					str(board[row][3]) + " " + str(board[row][4]) + " " + str(board[row][5]) + "|" + 
					str(board[row][6]) + " " + str(board[row][7]) + " " + str(board[row][8]))
		else:
			print(str(board[row][0]) + " " + str(board[row][1]) + " " + str(board[row][2]) + "|" +
					str(board[row][3]) + " " + str(board[row][4]) + " " + str(board[row][5]) + "|" + 
					str(board[row][6]) + " " + str(board[row][7]) + " " + str(board[row][8]))

# prints nicely formatted solution to stdout
def printSolution(result,count,board,filename):
	print("------------------")
	print("   SOLVED PUZZLE  ")
	print("------------------")
	if (result and count > 7):
		printBoard(board)
		print("# of var assignments= %i" % count)
	else:
		b = createBoard(filename)
		res, c = resolve(b, 0)
		printBoard(b)
		print("# of var assignments= %i" % c)

# check if num is valid in given row
def is_valid_in_row(num, row, board):
	for col in range(0,9):
		if(board[row][col] == num):
			return False

	return True

# check if num is valid in given column
def is_valid_in_col(num, col, board):
	for row in range(0,9):
		if(board[row][col] == num):
			return False

	return True

# helper function for is_valid_in_subgrid()
def check_subgrid(start_row,start_col,num, board):
	for row in range(0,3):
		for col in range(0,3):
			if(board[row + start_row][col + start_col] == num):
				return False

	return True 

# check if num is valid in 3x3 subgrid
def is_valid_in_subgrid(num, row, col, board):
	if (row < 3):
		if (col < 3):
			return check_subgrid(0,0,num,board)
		elif (col < 6):
			return check_subgrid(0,3,num,board)
		else:
			return check_subgrid(0,6,num,board)
	if (row < 6):
		if (col < 3):
			return check_subgrid(3,0,num,board)
		elif (col < 6):
			return check_subgrid(3,3,num,board)
		else:
			return check_subgrid(3,6,num,board)
	if (row < 9):
		if (col < 3):
			return check_subgrid(6,0,num,board)
		elif (col < 6):
			return check_subgrid(6,3,num,board)
		else:
			return check_subgrid(6,6,num,board)

# check if num is valid in given box 
def is_valid_in_box(num, row, col, board):

	subgrid_result = (is_valid_in_subgrid(num,row, col, board))
	col_result = (is_valid_in_col(num,col,board))
	row_result = (is_valid_in_row(num,row,board))

	return (row_result and col_result and subgrid_result)

# find unassigned box
def find_unassigned_box(board):
	for r in range(0,9):
		for c in range(0,9):
			if (0 == board[r][c]):
				row = r
				col = c 
				# found unassigned box at row,col
				return (row,col)
	
	# board has no unassigned boxes
	return (-1,-1)

# finds unassigned box/boxes with minimum remaining values
def mrv(dic,unassigned_boxes):
	min_val = 9
	for box in unassigned_boxes:
		if(dic[box][0] < min_val):
			min_val = dic[box][0]

	mrv_boxes = []
	for box in unassigned_boxes:
		if (dic[box][0] == min_val):
			mrv_boxes.append(box)

	return mrv_boxes

# helps resolve issues with printSolution()
def resolve(board,counter):
	row, col = find_unassigned_box(board)
	if (row == -1 and col == -1):
		return (True,counter)
	else:
		for num in range(1,10):
			if(is_valid_in_box(num, row, col, board)):
				board[row][col] = num 
				counter += 1          
				
				result, count = resolve(board, counter)
				if (result == False):
					board[row][col] = 0  
				else:
					return (True, count)
		
		return (False,counter)

# helper to get_degree()
def get_degree_helper(start_row,start_col,avoid_row,avoid_col,board,counter):
	for row in range(0,3):
		for col in range(0,3):
			r_sum = row + start_row
			c_sum = col + start_col
			if(board[r_sum][c_sum] == 0):
				if ((r_sum != avoid_row) or (c_sum != avoid_col)):
					counter += 1

	return counter

# helper to degree function - fetches contraining degree of a box
def get_degree(row,col,board):
	degree = 0

	for r in range(0,9):
		if (board[r][col] == 0):
			if(r != row):
				degree += 1

	for c in range(0,9):
		if (board[row][c] == 0):
			if(c != col):
				degree += 1

	if (row < 3):
		if (col < 3):
			return get_degree_helper(0,0,row,col,board,degree)
		elif (col < 6):
			return get_degree_helper(0,3,row,col,board,degree)
		else:
			return get_degree_helper(0,6,row,col,board,degree)
	if (row < 6):
		if (col < 3):
			return get_degree_helper(3,0,row,col,board,degree)
		elif (col < 6):
			return get_degree_helper(3,3,row,col,board,degree)
		else:
			return get_degree_helper(3,6,row,col,board,degree)
	if (row < 9):
		if (col < 3):
			return get_degree_helper(6,0,row,col,board,degree)
		elif (col < 6):
			return get_degree_helper(6,3,row,col,board,degree)
		else:
			return get_degree_helper(6,6,row,col,board,degree)
	

# finds unassigned box/boxes that is most constraining on other unassigned variables
def degree(mrv_boxes, board):
	if (len(mrv_boxes) == 1):
		return mrv_boxes[0]
	else:
		degree_boxes = {}
		for box in mrv_boxes:
			deg = get_degree(box[0],box[1],board)
			degree_boxes[box] = deg
		
		max_degree = 0
		for key in degree_boxes:
			if (degree_boxes[key] > max_degree):
				max_degree = degree_boxes[key]

		max_degree_boxes = []
		for key in degree_boxes:
			if (degree_boxes[key] == max_degree):
				max_degree_boxes.append(key)
		
		# if there 1 more than one option, we can arbitrarily pick a box
		# in this case we return the first box
		return max_degree_boxes[0]   

# finds the next unassigned based on MRV & Degree heuristic
def find_unassigned_box_hue(board,dic):
	unassigned_boxes = []
	for r in range(0,9):
		for c in range(0,9):
			if (0 == board[r][c]):
				unassigned_boxes.append((r,c))

	if (len(unassigned_boxes) == 0):
		return (-1,-1)
	else:
		mrv_boxes = mrv(dic,unassigned_boxes)
		return degree(mrv_boxes,board)

# initializes remaining values for a given box (row, col) in puzzle
def initialize_remaining_values(dic,board):
	for row in range(0,9):
		for col in range(0,9):
			if(board[row][col] == 0):
				dic[(row,col)] =  [9,[1,2,3,4,5,6,7,8,9]]
	
	for r in range(0,9):
		for c in range(0,9):
			if(board[r][c] == 0):
				for num in range(1,10):
					if(is_valid_in_box(num,r,c,board) != True):
						dic[(r,c)][0] -= 1
						dic[(r,c)][1][num-1] = -1

# removes number as possible value for a given box(row,col) and returns 
# False if no possible values left for given box, and True otherwise
def eliminate_value(num, row, col, dic):
	if (row,col) in dic:
		possible_values = dic[(row,col)]

		if (possible_values[1][num-1] != -1):
			possible_values[1][num-1] = -1    # set a value to -1 to indicate it's not a legal value anymore
			possible_values[0] -= 1           # decrement available value count
			dic[(row,col)] = possible_values  # update dic

		if (possible_values[0] == 0):
			return False
		else:
			return True

# reassigns previously removed number for a given box(row,col)
def reassign_value(num,row,col,dic):
	if (row,col) in dic:
		possible_values = dic[(row,col)]

		if (possible_values[1][num-1] == -1):
			possible_values[1][num-1] = num   # reassign value
			possible_values[0] += 1           # increment available value count
			dic[(row,col)] = possible_values  # update dic 

# removes number from possible values of all boxes in the same row
def eliminate_constraining_row(num, row, col, dic):
	for c in range(0,9):
		if (c != col):
			if(eliminate_value(num, row, c, dic) == False):
				return False
	return True

# reassigns number to possible values of all boxes in the same row
def reassign_constraining_row(num, row, col, dic):
	for c in range(0,9):
		if(c != col):
			reassign_value(num, row, c, dic)

# removes number from possible values of all boxes in the same col
def eliminate_constraining_col(num, row, col, dic):
	for r in range(0,9):
		if (r != row):
			if(eliminate_value(num, r, col, dic) == False):
				return False
	return True

# reassigns number to possible values of all boxes in the same col
def reassign_constraining_col(num, row, col, dic):
	for r in range(0,9):
		if (r != row):
			reassign_value(num, r, col, dic)

# helper function for eliminate_constraining_subgrid()
def eliminate_subgrid(start_row,start_col,avoid_row,avoid_col,num,dic):
	for row in range(0,3):
		for col in range(0,3):
			r = row + start_row
			c = col + start_col
			if(r != avoid_row or c != avoid_col):
				if(eliminate_value(num,r,c,dic) == False):
					return False
	return True

# helper function for reassign_constraining_subgrid()
def reassign_subgrid(start_row,start_col,avoid_row,avoid_col,num,dic):
	for row in range(0,3):
		for col in range(0,3):
			r = row + start_row
			c = col + start_col
			if (r != avoid_row or c != avoid_col):
				reassign_value(num,r,c,dic)

# rassigns number to possible values of all boxes in subgrid
def reassign_constraining_subgrid(num, row, col, dic):
	if (row < 3):
		if (col < 3):
			reassign_subgrid(0,0,row,col,num,dic)
		elif (col < 6):
			reassign_subgrid(0,3,row,col,num,dic)
		else:
			reassign_subgrid(0,6,row,col,num,dic)
	if (row < 6):
		if (col < 3):
			reassign_subgrid(3,0,row,col,num,dic)
		elif (col < 6):
			reassign_subgrid(3,3,row,col,num,dic)
		else:
			reassign_subgrid(3,3,row,col,num,dic)
	if (row < 9):
		if (col < 3):
			reassign_subgrid(6,0,row,col,num,dic)
		elif (col < 6):
			reassign_subgrid(6,3,row,col,num,dic)
		else:
			reassign_subgrid(6,6,row,col,num,dic)

# removes number from possible values of all boxes in subgrid
def eliminate_constraining_subgrid(num, row, col, dic):
	if (row < 3):
		if (col < 3):
			return eliminate_subgrid(0,0,row,col,num,dic)
		elif (col < 6):
			return eliminate_subgrid(0,3,row,col,num,dic)
		else:
			return eliminate_subgrid(0,6,row,col,num,dic)
	if (row < 6):
		if (col < 3):
			return eliminate_subgrid(3,0,row,col,num,dic)
		elif (col < 6):
			return eliminate_subgrid(3,3,row,col,num,dic)
		else:
			return eliminate_subgrid(3,6,row,col,num,dic)
	if (row < 9):
		if (col < 3):
			return eliminate_subgrid(6,0,row,col,num,dic)
		elif (col < 6):
			return eliminate_subgrid(6,3,row,col,num,dic)
		else:
			return eliminate_subgrid(6,6,row,col,num,dic)

# eliminate number from possible values for all constraining boxes
def eliminate_constraining_values(num, row, col, dic):
	subgrid_result = eliminate_constraining_subgrid(num,row,col,dic)
	col_result = eliminate_constraining_col(num,row,col,dic)
	row_result = eliminate_constraining_row(num,row,col,dic)
	return (subgrid_result and col_result and row_result)

# reassigns previously removed number to possible values for all constraining boxes
def reassign_constraining_values(num, row, col, dic):
	reassign_constraining_subgrid(num,row,col,dic)
	reassign_constraining_col(num,row,col,dic)
	reassign_constraining_row(num,row,col,dic)

# helper to get_lcv()
def get_lcv_helper(start_row,start_col,avoid_row,avoid_col,value,dic,counter):
	for row in range(0,3):
		for col in range(0,3):
			r_sum = row + start_row
			c_sum = col + start_col
			if ((r_sum != avoid_row) or (c_sum != avoid_col)):
				if((r_sum,c_sum) in dic):
					if(value in dic[(r_sum,c_sum)][1]):
						counter += 1
	return counter

# returns value that is least constraining
def get_lcv(value_options, row, col, dic):
	lcv_dict = {}
	for value in value_options:
		if (value != -1):
			counter = 0
			# check constraining row
			for c in range(0,9):
				if (c != col):
					if ((row,c) in dic):
						if (value in dic[(row,c)][1]):
							counter += 1
			
			# check constraining column
			for r in range(0,9):
				if (r != row):
					if ((r,col) in dic):
						if (value in dic[(r,col)][1]):
							counter += 1
			
			# check constraining subgrid
			if (row < 3):
				if (col < 3):
					counter = get_lcv_helper(0,0,row,col,value,dic,counter)
				elif (col < 6):
					counter = get_lcv_helper(0,3,row,col,value,dic,counter)
				else:
					counter = get_lcv_helper(0,6,row,col,value,dic,counter)
			if (row < 6):
				if (col < 3):
					counter = get_lcv_helper(3,0,row,col,value,dic,counter)
				elif (col < 6):
					counter = get_lcv_helper(3,3,row,col,value,dic,counter)
				else:
					counter = get_lcv_helper(3,6,row,col,value,dic,counter)
			if (row < 9):
				if (col < 3):
					counter = get_lcv_helper(6,0,row,col,value,dic,counter)
				elif (col < 6):
					counter = get_lcv_helper(6,3,row,col,value,dic,counter)
				else:
					counter = get_lcv_helper(6,6,row,col,value,dic,counter)
			
			# update lcv_dict with counter for each value
			lcv_dict[value] = counter

	# determine lcv
	min_count = 80
	for key in lcv_dict:
		if (lcv_dict[key] < min_count):
			min_count = lcv_dict[key]

	lcv_options = []
	for key in lcv_dict:
		if (lcv_dict[key] == min_count):
			lcv_options.append(key)

	# return lcv
	return lcv_options