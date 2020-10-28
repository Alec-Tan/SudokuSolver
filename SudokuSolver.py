import random

def newBlankBoard():
    return [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]

def newRandomBoard(numClues):  #numClues must be from [0, 81]
    board = newBlankBoard()
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        randIdx = random.randrange(len(numbers))
        board[0][i] = numbers.pop(randIdx)
    randomSolve(board)

    numRemovals = 81 - numClues
    filledIndices = []
    for n in range(81):
        filledIndices.append(n)
    for n in range(numRemovals):
        boardIdx = filledIndices.pop(random.randrange(len(filledIndices)))
        row = boardIdx // 9
        column = boardIdx % 9
        board[row][column] = 0
    return board

def printBoard(board):
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("- - - - - - - - - - - -")

        for column in range(9):
            if column % 3 == 0 and column != 0:
                print(" | ", end="")

            if column == 8:
                print(board[row][column])
            else:
                print(str(board[row][column]) + " ", end="")

def isUsedInRow(board, row, num):
    for column in range(9):
        if board[row][column] == num:
            return True
    return False

def isUsedInCol(board, column, num):
    for row in range(9):
        if board[row][column] == num:
            return True
    return False

def isUsedInBox(board, row, column, num):
    box_x = (column // 3) * 3
    box_y = (row // 3) * 3

    for row in range(3):
        for column in range(3):
            if board[box_y + row][box_x + column] == num:
                return True
    return False

def isValid(board, row, column, num):
    if isUsedInRow(board, row, num) == False and isUsedInCol(board, column, num) == False and isUsedInBox(board, row, column, num) == False:
        return True
    return False

def findEmpty(board):
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return (row, column)
    return None

def solve(board):
    find = findEmpty(board)
    if find == None:
        return True
    else:
        row = find[0]
        column = find[1]

    for num in range(1, 10):
        if isValid(board, row, column, num):
            board[row][column] = num

            if solve(board):
                return True

            board[row][column] = 0
    return False

# Same as solve() but tries random numbers in 1-10 rather than in order
def randomSolve(board):
    find = findEmpty(board)
    if find == None:
        return True
    else:
        row = find[0]
        column = find[1]

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for n in range(9):
        num = numbers.pop(random.randrange(len(numbers)))
        if isValid(board, row, column, num):
            board[row][column] = num

            if solve(board):
                return True

            board[row][column] = 0
    return False
