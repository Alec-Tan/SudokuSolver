import random


def new_blank_board():
    """
    Creates a new sudoku board with no numbers entered.

    Returns:
        List of List of int: A 2D array which represents a sudoku board.
    """

    return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]


def new_random_board(num_clues):
    """
    Creates a new sudoku board with random clues entered in.

    Parameters:
        num_clues (int): The number of clues which the board will have. Must be from [0, 81].

    Returns:
        List of List of int: A 2D array which represents a sudoku board.
    """

    board = new_blank_board()

    # Fill the first row of the board with random numbers from 1-9.
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        rand_idx = random.randrange(len(numbers))
        board[0][i] = numbers.pop(rand_idx)

    # Solve the board to get a complete and correct board.
    random_solve(board)

    # Remove numbers from the board to get only our desired number of clues.
    num_removals = 81 - num_clues
    filled_indices = []
    for n in range(81):
        filled_indices.append(n)
    # Remove numbers by setting their values to 0.
    for n in range(num_removals):
        board_idx = filled_indices.pop(random.randrange(len(filled_indices)))
        row = board_idx // 9
        column = board_idx % 9
        board[row][column] = 0
    return board


def is_used_in_row(board, row, num):
    """
    Checks to see if a number is already being used in a certain row.

    Parameters:
        board (List of List of int): A 2D array which represents a sudoku board.
        row (int): The row to be checked.
        num (int): The number that we want to see if it is already being used.

    Returns:
        bool: True if the number is being used in the row, False otherwise.
    """

    for column in range(9):
        if board[row][column] == num:
            return True
    return False


def is_used_in_col(board, column, num):
    """
    Checks to see if a number is already being used in a certain column.

    Parameters:
        board (List of List of int): A 2D array which represents a sudoku board.
        column (int): The column to be checked.
        num (int): The number that we want to see if it is already being used.

    Returns:
        bool: True if the number is being used in the column, False otherwise.
    """

    for row in range(9):
        if board[row][column] == num:
            return True
    return False


def is_used_in_box(board, row, column, num):
    """
    Checks to see if a number is already being used in a certain 3x3 box.

    Parameters:
        board (List of List of int): A 2D array which represents a sudoku board.
        row (int): The row to be checked.
        column (int): The column to be checked.
        num (int): The number that we want to see if it is already being used.

    Returns:
        bool: True if the number is being used in the 3x3 box, False otherwise.
    """

    # Calculate the indices of the top-left cell of the 3x3 box.
    box_x = (column // 3) * 3
    box_y = (row // 3) * 3

    for row in range(3):
        for column in range(3):
            if board[box_y + row][box_x + column] == num:
                return True
    return False


def is_valid(board, row, column, num):
    """
    Checks to see if a number in a specified position is valid according to the rules of sudoku.

    A number is valid if it is unique for its row, column, and 3x3 box.

    Parameters:
        board (List of List of int): A 2D array which represents a sudoku board.
        row (int): The row to be checked.
        column (int): The column to be checked.
        num (int): The number to be checked.

    Returns:
        bool: True if the number is being used in the 3x3 box, False otherwise.
    """

    if not is_used_in_row(board, row, num) and not is_used_in_col(board, column, num) \
            and not is_used_in_box(board, row, column, num):
        return True
    return False


def find_empty(board):
    """
    Finds the first cell (row, column) in a board that is empty.

    A cell is empty if it is 0.

    Parameters:
        board (List of List of int): A 2D array which represents a sudoku board.

    Returns:
        tuple: Contains the indices (row, column). Returns None if there is not an empty cell.
    """

    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return (row, column)
    return None


def solve(board):
    """
    Recursively solves a sudoku board using the backtracking algorithm.

    Parameters:
        board (List of List of int): A 2D array which represents a sudoku board.

    Returns:
        bool: True if the board is solved. Returns False if there are no valid numbers for a cell and retries.
    """

    find = find_empty(board)
    if find is None:
        return True
    else:
        row = find[0]
        column = find[1]

    for num in range(1, 10):
        if is_valid(board, row, column, num):
            board[row][column] = num

            if solve(board):
                return True

            board[row][column] = 0
    return False


def random_solve(board):
    """Same as solve() but tries random numbers in 1-10 rather than in order."""
    find = find_empty(board)
    if find is None:
        return True
    else:
        row = find[0]
        column = find[1]

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for n in range(9):
        num = numbers.pop(random.randrange(len(numbers)))
        if is_valid(board, row, column, num):
            board[row][column] = num

            if solve(board):
                return True

            board[row][column] = 0
    return False
