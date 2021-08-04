import pygame


class BoardCell:
    """
    This class represents one cell/box on a sudoku board.

    Attributes:
        number (int): The number contained in this cell.
        row (int): The row number in which this cell is located.
        column (int): The column number in which this cell is located.
        width (int): How many pixels wide the cell will be when drawn.
        height (int): How many pixels high the cell will be when drawn.
        font (pygame.font.SysFont): The font for the number.
        blank (pygame.Surface): A blank Surface that will have black borders.
    """

    def __init__(self, number, row, column, width, height):
        """
        The constructor for a BoardCell.

        Parameters:
            number (int): The number contained in this cell.
            row (int): The row number in which this cell is located.
            column (int): The column number in which this cell is located.
            width (int): How many pixels wide the cell will be when drawn.
            height (int): How many pixels high the cell will be when drawn.
        """

        self.number = number
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Comic Sans MS', 50)
        self.blank = pygame.Surface((self.width, self.height))
        self.blank.fill((255, 255, 255))

        # Determine thickness of the top and bottom lines.
        if row in [2, 5, 8]:  # Bottom needs to be thick because the cell is on the bottom row of a 3x3 box.
            bottom_thickness = 5
            top_thickness = 1
        elif row in [3, 6]:  # Top needs to be thick because the cell is on the the top row of a 3x3 box.
            bottom_thickness = 1
            top_thickness = 5
        else:
            bottom_thickness = 1
            top_thickness = 1

        # Determine thickness of left and right lines.
        if column in [2, 5]:  # Right needs to be thick because the cell is on the rightmost column of a 3x3 box.
            right_thickness = 5
            left_thickness = 1
        elif column in [3, 6]:  # Left needs to be thick because the cell is on the leftmost column of a 3x3 box.
            right_thickness = 1
            left_thickness = 5
        else:
            right_thickness = 1
            left_thickness = 1

        # Draws the lines of the cell on a blank Surface
        pygame.draw.line(self.blank, (0, 0, 0), (0, 0), (width, 0), top_thickness)  # top line
        pygame.draw.line(self.blank, (0, 0, 0), (0, 0), (0, height), left_thickness)  # left line
        pygame.draw.line(self.blank, (0, 0, 0), (0, height), (width, height), bottom_thickness)  # bottom line
        pygame.draw.line(self.blank, (0, 0, 0), (width, 0), (width, height), right_thickness)  # right line

    def draw_blank(self, screen):
        """
        Draws a white/blank box with black borders around it at the cell's position.

        Parameters:
            screen (Surface): A surface which will be drawn on.
        """

        screen.blit(self.blank, (self.column * self.width, self.row * self.height))
        
    def draw(self, screen):
        """
        Draws the BoardCell's number with black borders around it at the cell's position.

        Parameters:
            screen (Surface): A surface which will be drawn on.
        """

        # Erase anything that was drawn at this cell's position previously.
        self.draw_blank(screen)

        # Draw the cell onto the screen.
        text_surface = self.font.render(str(self.number), False, (0, 0, 0))
        screen.blit(text_surface, (self.column * self.width + self.width / 3, self.row * self.height))