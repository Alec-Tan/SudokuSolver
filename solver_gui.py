import pygame
import solver
import pygame_textinput
from board_cell import BoardCell


class Grid:
    """
    This class represents a sudoku board/grid.

    Attributes:
        width (int): How many pixels wide the grid will be when drawn.
        height (int): How many pixels high the grid will be when drawn.
        screen (Surface): A surface which will be drawn on.
        board (List of List of int): A 2D array which represents a sudoku board.
        cells (List of List of BoardCell): A 2D array of BoardCells that represents a sudoku board.
    """

    def __init__(self, width, height, screen, num_clues=30):
        """
        The constructor for a Grid

        Parameters:
            width (int): How many pixels wide the grid will be when drawn.
            height (int): How many pixels high the grid will be when drawn.
            screen (Surface): A surface which will be drawn on.
            num_clues (int): The number of clues which the board will have. Must be from [0, 81].
        """

        self.width = width
        self.height = height
        self.screen = screen
        self.board = solver.new_random_board(num_clues)
        self.cells = self.initialize_cells()

    def new_board(self, num_clues):
        """
        Creates a new board and new cells.

        Parameters:
            num_clues (int): The number of clues which the board will have. Must be from [0, 81].
        """

        self.board = solver.new_random_board(num_clues)
        self.cells = self.initialize_cells()

    def initialize_cells(self):
        """Initializes cells by filling the 2D array with BoardCells"""
        cells = self.board
        for row in range(9):
            for column in range(9):
                cells[row][column] = BoardCell(self.board[row][column], row, column, self.width // 9, self.width // 9)
        return cells

    def draw_clues(self):
        """Draws all clues onto the screen."""
        for row in range(9):
            for column in range(9):
                self.cells[row][column].draw_blank(self.screen)
                if self.cells[row][column].number != 0:
                    self.cells[row][column].draw(self.screen)

    def solve(self):
        """Recursively solves a sudoku board using the backtracking algorithm."""
        find = find_empty(self.cells)
        if find is None:
            return True
        else:
            row = find[0]
            column = find[1]

        for num in range(1, 10):
            if is_valid(self.cells, row, column, num):
                self.cells[row][column].number = num
                self.cells[row][column].draw(self.screen)
                pygame.display.update()
                pygame.time.delay(3)

                if self.solve():
                    return True

                self.cells[row][column].number = 0
                self.cells[row][column].draw_blank(self.screen)
                pygame.display.update()
                pygame.time.delay(3)
        return False


# Functions for Grid's solve method
def is_used_in_row(cells, row, num):
    """
    Checks to see if a number is already being used in a certain row.

    Parameters:
        cells (List of List of BoardCell): A 2D array of BoardCells that represents a sudoku board.
        row (int): The row to be checked.
        num (int): The number that we want to see if it is already being used.

    Returns:
        bool: True if the number is being used in the row, False otherwise.
    """

    for column in range(9):
        if cells[row][column].number == num:
            return True
    return False


def is_used_in_col(cells, column, num):
    """
    Checks to see if a number is already being used in a certain column

    Parameters:
        cells (List of List of BoardCell): A 2D array of BoardCells that represents a sudoku board.
        column (int): The column to be checked.
        num (int): The number that we want to see if it is already being used.

    Returns:
        bool: True if the number is being used in the column, False otherwise.
    """

    for row in range(9):
        if cells[row][column].number == num:
            return True
    return False


def is_used_in_box(cells, row, column, num):
    """
    Checks to see if a number is already being used in a certain 3x3 box.

    Parameters:
        cells (List of List of BoardCell): A 2D array of BoardCells that represents a sudoku board.
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
            if cells[box_y + row][box_x + column].number == num:
                return True
    return False


def is_valid(cells, row, column, num):
    """
    Checks to see if a number in a specified position is valid according to the rules of sudoku.

    A number is valid if it is unique for its row, column, and 3x3 box.

    Parameters:
        cells (List of List of BoardCell): A 2D array of BoardCells that represents a sudoku board.
        row (int): The row to be checked.
        column (int): The column to be checked.
        num (int): The number to be checked.

    Returns:
        bool: True if the number is being used in the 3x3 box, False otherwise.
    """

    if not is_used_in_row(cells, row, num) and not is_used_in_col(cells, column, num)\
            and not is_used_in_box(cells, row, column, num):
        return True
    return False


def find_empty(cells):
    """
    Finds the first cell (row, column) in a board that is empty.

    A cell is empty if it is 0.

    Parameters:
        cells (List of List of BoardCell): A 2D array of BoardCells that represents a sudoku board.

    Returns:
        tuple: Contains the indices (row, column). Returns None if there is not an empty cell.
    """

    for row in range(9):
        for column in range(9):
            if cells[row][column].number == 0:
                return (row, column)
    return None


def main():
    pygame.init()
    sc_width = 720
    sc_height = 800
    screen = pygame.display.set_mode((sc_width, sc_height))
    pygame.display.set_caption("Sudoku Generator & Solver")
    grid_width = 720
    grid_height = 720
    height_diff = sc_height - grid_height
    font = pygame.font.SysFont('Comic Sans MS', 20)
    white = (255, 255, 255)
    clock = pygame.time.Clock()
    run = True

    # Button to create a new board
    new_board_button = pygame.Rect(sc_width * 2.5/5, grid_height + height_diff / 4, sc_width / 7, height_diff / 2)
    new_board_text = font.render("New Board", False, (0, 0, 0))

    # Button to solve the current board
    solve_button = pygame.Rect(sc_width * 3.5/5, grid_height + height_diff / 4, sc_width / 7, height_diff / 2)
    solve_text = font.render("Solve", False, (0, 0, 0))

    # Text field for number of clues
    text_input = pygame_textinput.TextInput("30")
    clues_text = font.render("Number of Clues: ", False, (0, 0, 0))

    # Generate a starting sudoku board
    grid = Grid(grid_width, grid_height, screen)

    while run:
        screen.fill(white)
        grid.draw_clues()
        clock.tick(30)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check if user clicks on the new board button or the solve button.
                if new_board_button.collidepoint(mouse_pos):
                    try:
                        # Generate new board based on user input.
                        user_input = int(text_input.get_text())
                        if user_input <= 81 and user_input > 0:
                            grid.new_board(user_input)
                            grid.draw_clues()
                        else:
                            text_input.clear_text()
                    except:
                        text_input.clear_text()
                elif solve_button.collidepoint(mouse_pos):
                    grid.solve()

        # Draw button to generate a new board and its text
        pygame.draw.rect(screen, (105, 105, 105), new_board_button)
        screen.blit(new_board_text, (sc_width * 2.5 / 5, grid_height + height_diff / 4))

        # Draw button to solve board and its text
        pygame.draw.rect(screen, (105, 105, 105), solve_button)
        screen.blit(solve_text, (sc_width * 3.5 / 5 + sc_width / 30, grid_height + height_diff / 4))

        # Update the TextInput object and number of clues text and display them
        text_input.update(events)
        screen.blit(text_input.get_surface(), (sc_width / 3, grid_height + height_diff / 3))
        screen.blit(clues_text, (sc_width / 10, grid_height + height_diff / 4))

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
