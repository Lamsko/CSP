import numpy as np
import pandas as pd
import time
from IPython.display import display

def isCorrect(grid, row, column):
	return isRowCorrect(grid, row) and isColumnCorrect(grid, column) and isDiagonalCorrect(grid, row, column)


def isRowCorrect(grid, row):
	for col in range(len(grid)):
		if grid[row, col] == 1:
			return False
	return True


def isColumnCorrect(grid, column):
	for row in range(len(grid)):
		if grid[row, column] == 1:
			return False
	return True


def checkUpperDiagonal(grid, row, column):
	iterRow = row
	iterCol = column
	while iterCol >= 0 and iterRow >= 0:
		if grid[iterRow, iterCol] == 1:
			return False
		iterCol -= 1
		iterRow -= 1
	return True


def checkLowerDiagonal(grid, row, column):
	iterRow = row
	iterCol = column
	while iterCol >= 0 and iterRow < len(grid):
		if grid[iterRow, iterCol] == 1:
			return False
		iterRow += 1
		iterCol -= 1
	return True


def isDiagonalCorrect(grid, row, column):
	return checkUpperDiagonal(grid, row, column) and checkLowerDiagonal(grid, row, column)


N = 20
n_queen_table = np.array(np.zeros(shape = (N,N), dtype=int))


def getProposition(board, column):
	rows = []
	for row in range(len(board)):
		if isCorrect(board, row, column):
			rows.append(row)
	return rows


def solveBacktracking(board, column):
	if len(board) == column:
		return True
	rows_proposal = getProposition(board, column)
	for row in rows_proposal:
		if isCorrect(board, row, column):
			board[row, column] = 1
			if solveBacktracking(board, column + 1):
				return True
			board[row, column] = 0
	return False


def getUnassignedFromConstraint(board, column):
	result = [[] for _ in range(column+1, len(board))]
	for row in range(len(board)):
		for col in range(column+1, len(board)):
			if board[row, col] == 0 and isCorrect(board, row, col):
				result[col - (column + 1)] = (row, col)
	return result


def solveForwardChecking(board, column):
	if len(board) == column:
		return True
	rows_proposal = getProposition(board, column)
	for row in rows_proposal:
		board[row, column] = 1
		domain_wipe_out = False
		un_list = getUnassignedFromConstraint(board, column)
		for q_proposal in un_list:
			if not q_proposal:
				domain_wipe_out = True
				break
		if not domain_wipe_out:
			if solveForwardChecking(board, column + 1):
				return True
		board[row, column] = 0
	return False


# start = time.time()
# solveBacktracking(n_queen_table, 0)
# pd_result = pd.DataFrame(data=n_queen_table, index=range(N), columns=range(N))
# display(pd_result)
# end = time.time()
# print(end - start)
print()
start = time.time()
solveForwardChecking(n_queen_table, 0)
pd_result = pd.DataFrame(data=n_queen_table, index=range(N), columns=range(N))
display(pd_result)
end = time.time()
print(end - start)