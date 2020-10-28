import pygame
import SudokuSolver as solver
import pygame_textinput
from BoardCell import BoardCell


class Grid:
    def __init__(self, width, height, screen, numClues=30):
        self.width = width
        self.height = height
        self.screen = screen
        self.board = solver.newRandomBoard(numClues)
        self.cells = self.initializeCells()

    def newBoard(self, numClues):
        self.board = solver.newRandomBoard(numClues)
        self.cells = self.initializeCells()

    def initializeCells(self):
        cells = self.board
        for row in range(9):
            for column in range(9):
                cells[row][column] = BoardCell(self.board[row][column], row, column, self.width / 9, self.width / 9)
        return cells

    def drawClues(self):
        for row in range(9):
            for column in range(9):
                self.cells[row][column].drawBlank(self.screen)
                if self.cells[row][column].number != 0:
                    self.cells[row][column].draw(self.screen)

    def solve(self):
        find = findEmpty(self.cells)
        if find == None:
            return True
        else:
            row = find[0]
            column = find[1]

        for num in range(1, 10):
            if isValid(self.cells, row, column, num):
                self.cells[row][column].number = num
                self.cells[row][column].draw(self.screen)
                pygame.display.update()
                pygame.time.delay(30)

                if self.solve():
                    return True

                self.cells[row][column].number = 0
                self.cells[row][column].drawBlank(self.screen)
                pygame.display.update()
                pygame.time.delay(30)
        return False


# Functions for Grid's solve method
def isUsedInRow(cells, row, num):
    for column in range(9):
        if cells[row][column].number == num:
            return True
    return False

def isUsedInCol(cells, column, num):
    for row in range(9):
        if cells[row][column].number == num:
            return True
    return False

def isUsedInBox(cells, row, column, num):
    box_x = (column // 3) * 3
    box_y = (row // 3) * 3

    for row in range(3):
        for column in range(3):
            if cells[box_y + row][box_x + column].number == num:
                return True
    return False

def isValid(cells, row, column, num):
    if (isUsedInRow(cells, row, num) == False and isUsedInCol(cells, column, num) == False
            and isUsedInBox(cells, row, column, num) == False):
        return True
    return False

def findEmpty(cells):
    for row in range(9):
        for column in range(9):
            if cells[row][column].number == 0:
                return (row, column)
    return None


def main():
    pygame.init()
    scWidth = 720
    scHeight = 800
    screen = pygame.display.set_mode((scWidth, scHeight))
    pygame.display.set_caption("Sudoku Generator & Solver")
    gridWidth = 720
    gridHeight = 720
    heightDiff = scHeight - gridHeight
    font = pygame.font.SysFont('Comic Sans MS', 20)
    white = (255, 255, 255)
    clock = pygame.time.Clock()
    run = True

    # Button to create a new board
    newBoardButton = pygame.Rect(scWidth * 2.5/5, gridHeight + heightDiff / 4, scWidth / 7, heightDiff / 2)
    newBoardText = font.render("New Board", False, (0, 0, 0))

    # Button to solve the current board
    solveButton = pygame.Rect(scWidth * 3.5/5, gridHeight + heightDiff / 4, scWidth / 7, heightDiff / 2)
    solveText = font.render("Solve", False, (0, 0, 0))

    # Text field for number of clues
    textInput = pygame_textinput.TextInput("30")
    cluesText = font.render("Number of Clues: ", False, (0, 0, 0))

    # Generate a starting sudoku board
    grid = Grid(gridWidth, gridHeight, screen)

    while run:
        screen.fill(white)
        grid.drawClues()
        clock.tick(30)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos

                if newBoardButton.collidepoint(mousePos):
                    try:
                        input = int(textInput.get_text())
                        if input <= 81 and input > 0:
                            grid.newBoard(input)
                            grid.drawClues()
                        else:
                            textInput.clear_text()
                    except:
                        textInput.clear_text()
                elif solveButton.collidepoint(mousePos):
                    grid.solve()

        # Draw button to generate a new board and its text
        pygame.draw.rect(screen, (105, 105, 105), newBoardButton)
        screen.blit(newBoardText, (scWidth * 2.5 / 5, gridHeight + heightDiff / 4))

        # Draw button to solve board and its text
        pygame.draw.rect(screen, (105, 105, 105), solveButton)
        screen.blit(solveText, (scWidth * 3.5 / 5 + scWidth / 30, gridHeight + heightDiff / 4))

        # Update the TextInput object and number of clues text and display them
        textInput.update(events)
        screen.blit(textInput.get_surface(), (scWidth / 3, gridHeight + heightDiff / 3))
        screen.blit(cluesText, (scWidth / 10, gridHeight + heightDiff / 4))

        pygame.display.update()

    pygame.quit()

main()
