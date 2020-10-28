import pygame

class BoardCell:
    def __init__(self, number, row, column, width, height):
        self.number = number
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Comic Sans MS', 50)
        self.blank = pygame.Surface((self.width, self.height))
        self.blank.fill((255, 255, 255))

        # Determine thickness of top and bottom lines
        if row in [2, 5, 8]:   #bottom needs to be thick
            bottomThickness = 5
            topThickness = 1
        elif row in [3, 6]: #top needs to be thick
            bottomThickness = 1
            topThickness = 5
        else:
            bottomThickness = 1
            topThickness = 1

        # Determine thickness of left and right lines
        if column in [2, 5]:    #right needs to be thick
            rightThickness = 5
            leftThickness = 1
        elif column in [3, 6]:  #left needs to be thick
            rightThickness = 1
            leftThickness = 5
        else:
            rightThickness = 1
            leftThickness = 1

        # Draws the lines on the blank Surface
        pygame.draw.line(self.blank, (0, 0, 0), (0, 0), (width, 0), topThickness)  #top line
        pygame.draw.line(self.blank, (0, 0, 0), (0, 0), (0, height), leftThickness) #left line
        pygame.draw.line(self.blank, (0, 0, 0), (0, height), (width, height), bottomThickness) #bottom line
        pygame.draw.line(self.blank, (0, 0, 0), (width, 0), (width, height), rightThickness) #right line

    # Draws a white box with black borders around it
    def drawBlank(self, screen):
        screen.blit(self.blank, (self.column * self.width, self.row * self.height))
        
    def draw(self, screen):
        self.drawBlank(screen)
        
        textSurface = self.font.render(str(self.number), False, (0, 0, 0))
        screen.blit(textSurface, (self.column * self.width + self.width / 3, self.row * self.height))