# *************************************************************************
#  File    : SudokuSolver.py
#  Author  : Tanmay
# *************************************************************************

import csv
from statistics import mean
from SudokuHelper import *
from random import *

# solve sudoku puzzle using backtracking
def solve_A(board,counter):
	if(counter <= 10000):
		row, col = find_unassigned_box(board)
		 
		# board is completely filled
		if (row == -1 and col == -1):
			return (True,counter)

		else:
			for num in range(1,10):
				if(is_valid_in_box(num, row, col, board)):
					board[row][col] = num #temporarily assign num
					counter += 1          #update counter
					
					# recursive step
					result, count = solve_A(board, counter)
					if (result == False):
						board[row][col] = 0  #reset assignment 
					else:
						return (True, count)
			
			# backtrack
			return (False,counter)
	
	else:
		print("over 10,000 var assignments, terminating sudoku solver")
		exit()

# solve sudoku using forward checking + backtracking
def solve_B(board,counter,dic):
	if(counter <= 10000):
		row, col = find_unassigned_box(board)

		# board is completely filled
		if (row == -1 and col == -1):
			return (True,counter,dic)

		else:
			remaining_values = dic[(row,col)][1]
			for num in remaining_values:
				if (num != -1):
					if(is_valid_in_box(num,row,col,board)):
						if(eliminate_constraining_values(num,row,col,dic)):
							board[row][col] = num   #tentative assignment
							counter += 1            #update var counter
							  
							# recursive step
							result, c, d = solve_B(board,counter,dic)
							if (result):
								return(True,c,d)
							else:
								board[row][col] = 0 #reset assignment
								reassign_constraining_values(num,row,col,dic)
						else:
							reassign_constraining_values(num,row,col,dic)
			# backtrack
			return (False,counter,dic)
	else:
		print("over 10,000 var assignments, terminating sudoku solver")
		exit()

# solve sudoku using forward checking + backtracking + heuristics
def solve_C(board,counter,dic):
	if(counter <= 10000):
		row, col = find_unassigned_box_hue(board,dic)

		# board is completely filled
		if (row == -1 and col == -1):
			return (True,counter,dic)

		else:
			remaining_values = dic[(row,col)][1]
			lcv_options = get_lcv(remaining_values,row,col,dic)
			for num in lcv_options:
				if (num != -1):
					if(is_valid_in_box(num,row,col,board)):
						if(eliminate_constraining_values(num,row,col,dic)):
							board[row][col] = num   #tentative assignment
							counter += 1            #update var counter
							  
							# recursive step
							result, c, d = solve_C(board,counter,dic)
							if (result):
								return(True,c,d)
							else:
								board[row][col] = 0 #reset assignment
								reassign_constraining_values(num,row,col,dic)
						else:
							reassign_constraining_values(num,row,col,dic)
			# backtrack
			return (False,counter,dic)
	else:
		print("over 10,000 var assignments, terminating sudoku solver")
		exit()


# Main function to initiate Sudoku Solver
def main():
	# get sudoku puzzle to solve from test file
	try:
		filename = getTestFile()
		print("Which version/algorithm would you like to use to solve the sudoku puzzle?")
		version = input("Enter either A, B, or C: ")

		while (version.upper() not in ['A','B','C']):
			version = input("Invalid version. Enter either A, B, or C: ")
	except:
		exit()

	# create boards
	board_A = createBoard(filename) # backtracking
	board_B = createBoard(filename) # backtracking + forward checking
	board_C = createBoard(filename) # backtracking + forward checking + heuristics
 
	# dictionary storing possible values
	possibilities_B = {}
	possibilities_C = {}
	initialize_remaining_values(possibilities_B,board_B)
	initialize_remaining_values(possibilities_C,board_C)
	
	# solve + print sudoku puzzle depending on version
	if (version.upper() == 'A'):
		result_A, A_count = solve_A(board_A, 0)
		printSolution(result_A,A_count,board_A,filename)
		
	if (version.upper() == 'B'):
		result_B, B_count, possibilities_B_result = solve_B(board_B, 0, possibilities_B)
		printSolution(result_B,B_count,board_B,filename)

	if (version.upper() == 'C'):
		result_C, C_count, possibilities_C_result = solve_C(board_C, 0, possibilities_C)
		printSolution(result_C,C_count,board_C,filename)

# use for fetching & writing results to csv
def bulkTest():

	# open csv file to write to 
	with open('results.csv', mode='w', newline='') as csv_file:
		fieldnames = ['ALGO_TYPE','INITIAL VALUE','AVG ASSIGNMENT COUNT']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
	
		# iterate through all the test files
		for i in range(1,72):
			results = []
			for t in range(1,11):
				if (i,t) not in [(14,4),(15,2)]:
					filename = "sudoku_problems\\" + str(i) + "\\" + str(t) + ".sd"

					# create boards
					board_A = createBoard(filename)
					board_B = createBoard(filename)
					board_C = createBoard(filename)

					# dictionary storing possible values
					possibilities_B = {}
					possibilities_C = {}
					initialize_remaining_values(possibilities_B,board_B)
					initialize_remaining_values(possibilities_C,board_C)

					#solve using backtracking
					result, A_count = solve_A(board_A, 0)
					results.append(A_count)
					
					# solve using backtracking + forward checking
					#result, B_count, B_dict = solve_B(board_B, 0, possibilities_B)
					#results.append(B_count)
					
					# solve using backtracking + forward checking + heuristics
					#result, C_count, C_dict = solve_C(board_C, 0, possibilities_C)
					#results.append(C_count)

					# write results to csv file
					print("Initial Value: %i, Test File: %i, Assign Count: %i" % (i,t,A_count))
			
			avg_count = round(mean(results),2)
			writer.writerow({'ALGO_TYPE': 'Version A', 'INITIAL VALUE': i, 'AVG ASSIGNMENT COUNT': avg_count})

	print("done testing")

# Comment/Uncomment depending on goal:
main()      #if goal is to solve 1 sudoku puzzle
#bulkTest() #if goal is to solve all test sudoku puzzles