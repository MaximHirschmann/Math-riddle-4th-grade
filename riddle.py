# differentiate update and setup
import pygame
import sys
from random import randrange

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Math Grid")
        screenInfo = pygame.display.Info()
        self.width = screenInfo.current_w
        self.height = screenInfo.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.boardSize = self.height
        self.dimension = 8
        self.squareSize = self.boardSize/self.dimension
        self.outside = pygame.Rect(self.boardSize, 0, self.width-self.boardSize, self.boardSize)
        self.horizontal = {"A": (0, 0), "C":(5, 0), "E":(0, 2), "F":(4,2), "K":(5, 4), "O":(0, 6), "P":(4, 6), "Q":(3, 7)}
        self.vertical = {"B":(2, 0), "D":(7, 0), "G:":(6, 2), "H":(0, 3), "I":(3,3), "J":(2, 4), "L":(1, 5), "M": (4, 5), "N":(7, 5)}
        self.letters = [
            ["A", "", "B", "", "", "C", "", "D"],
            ["", "", "", "", "", "", "", ""],
            ["E", "", "", "", "F", "", "G", ""],
            ["H", "", "", "I", "", "", "", ""],
            ["", "", "J", "", "", "K", "", ""],
            ["", "L", "", "", "M", "", "", "N"],
            ["O", "", "", "", "P", "", "", ""],
            ["", "", "", "Q", "", "", "", ""],
        ]
        self.board = [
            ["", "", "", "", "x", "", "", ""],
            ["x", "x", "", "x", "x", "x", "x", ""],
            ["", "", "", "x", "", "", "", ""],
            ["", "x", "x", "", "x", "x", "", ""],
            ["", "x", "", "", "x", "", "", "x"],
            ["x", "", "", "x", "", "x", "", ""],
            ["", "", "", "x", "", "", "x", ""],
            ["x", "", "x", "", "", "", "", "x"],
        ]
        self.solution = self.generateSolution()
        for i in self.solution:
            print(i)
        self.horizontalTasks = []
        self.verticalTasks = []
        self.generateTasks()
        self.currentlySelected = None
        self.fontName = "Helvetica"
        self.fontSmall = pygame.font.SysFont(self.fontName, self.boardSize//24)
        self.fontMedium = pygame.font.SysFont(self.fontName, self.boardSize//15)
        self.fontBig = pygame.font.SysFont(self.fontName, self.boardSize//10)
        self.lineSize = self.boardSize//80
        self.colorLines = 0, 0, 0
        self.colorBackground = 255, 255, 255
        self.colorBlocked = 20, 33, 61
        self.colorSelected = 252, 163, 17
        self.colorFont = 20, 33, 61
        self.colorButton = 252, 163, 17
        self.colorCorrect = (129, 178, 154)
        self.colorFalse = (224, 122, 95)
        self.colorCell = 255, 255, 255
        self.timer = pygame.Rect(0, 0, self.outside.width//3, self.outside.height//12)
        self.timer.center = (self.outside.width//4 + self.boardSize, self.height * 11/12)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.seconds = 0
        self.buttCheck = pygame.Rect(0, 0, self.outside.width//3, self.outside.height//12)
        self.buttCheck.center = (self.outside.width*3/4 + self.boardSize, self.height * 11/12)

    """
    # Decided to use fullscreen mode
    def newSize(self, size):
        pygame.display.set_mode(size, pygame.RESIZABLE)
        self.width, self.height = size
        self.boardSize = size[1]
        self.squareSize = self.boardSize/self.dimension
        self.outside = pygame.Rect(self.boardSize, 0, self.width-self.boardSize, self.boardSize)
        self.fontSmall = pygame.font.SysFont(self.fontName, self.boardSize//20)
        self.fontMedium = pygame.font.SysFont(self.fontName, self.boardSize//15)
        self.fontBig = pygame.font.SysFont(self.fontName, self.boardSize//10)
        self.timer = pygame.Rect(0, 0, self.outside.width//3, self.outside.height//12)
        self.timer.center = (self.outside.width//4 + self.boardSize, self.height * 11/12)
        self.buttCheck = pygame.Rect(0, 0, self.outside.width//3, self.outside.height//12)
        self.buttCheck.center = (self.outside.width*3/4 + self.boardSize, self.height * 11/12)
        self.setup()
    """

    def generateSolution(self):
        solution = []
        for i in range(self.dimension):
            row = []
            for j in range(self.dimension):
                if self.board[i][j] != "x":
                    if self.letters[i][j]:
                        num = randrange(1, 10)
                    else:
                        num = randrange(0, 10)
                    row.append(str(num))
                else:
                    row.append("x")
            solution.append(row)
        return solution

    def getCoordinates(self, pos):
        x, y = pos
        return x*self.dimension//self.boardSize, y*self.dimension//self.boardSize

    def click(self):
        movesurface = self.fontSmall.render("0 s", True, self.colorFont)
        textRect = movesurface.get_rect(center = self.timer.center)
        self.screen.blit(movesurface, textRect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                        pygame.quit
                        sys.exit()
                    elif pygame.K_0 <= event.key <= pygame.K_9:
                        if self.currentlySelected:
                            i, j = self.currentlySelected
                            self.board[j][i] = event.unicode
                            self.setup()
                    elif pygame.K_BACKSPACE == event.key:
                        i, j = self.currentlySelected
                        self.board[j][i] = ""
                        self.setup()
                elif event.type == pygame.USEREVENT:
                    self.seconds += 1
                    self.updateTimer()
                    pygame.display.update()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.buttCheck.collidepoint(pos):
                        self.drawCorrect()
                        self.drawBoard()
                    else:
                        coordinates = self.getCoordinates(pos)
                        # on grid
                        if all(coordinates[i] < self.dimension for i in range(2)):
                            if self.currentlySelected == coordinates:
                                self.currentlySelected = None
                            else:
                                self.currentlySelected = coordinates
                            self.setup()
                            pygame.display.update()
                # elif event.type == pygame.VIDEORESIZE:
                #     size = event.size
                #     self.newSize(size)

    def updateTimer(self):
        text = ""
        if self.seconds >= 60:
            text += str(self.seconds//60) + " min : "
        text += str(self.seconds%60) + " s"
        pygame.draw.rect(self.screen, self.colorBackground, self.timer)
        movesurface = self.fontSmall.render(text, True, self.colorFont)
        textRect = movesurface.get_rect(center = self.timer.center)
        self.screen.blit(movesurface, textRect)

    def drawCorrect(self):
        if self.currentlySelected:
            self.currentlySelected = None
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i][j] != "x" and self.board[i][j] != "":
                    if self.board[i][j] == self.solution[i][j]:
                        color = self.colorCorrect
                    else:
                        color = self.colorFalse
                    pygame.draw.rect(
                        self.screen,
                        color,
                        [
                            j * self.squareSize,
                            i * self.squareSize,
                            self.squareSize,
                            self.squareSize
                        ]
                    )
                
    def updateSelected(self):
        pygame.draw.rect(
            self.screen,
            self.colorSelected,
            [
                round(self.currentlySelected[0]*self.squareSize), 
                round(self.currentlySelected[1]*self.squareSize),
                round(self.squareSize),
                round(self.squareSize)    
            ]
        )
        
    def drawBoard(self):
        # mark selected square
        if self.currentlySelected:
            self.updateSelected()
        # mark blocked squares:
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == "x":
                    pygame.draw.rect(
                        self.screen,
                        self.colorBlocked,
                        [
                            round(self.squareSize * j),
                            round(self.squareSize * i),
                            round(self.squareSize),
                            round(self.squareSize),
                        ]
                    )
        
        for i in range(self.dimension):
            for j in range(self.dimension):
                # add Letters
                if self.letters[i][j]:
                    movesurface = self.fontSmall.render(self.letters[i][j], True, self.colorFont)
                    self.screen.blit(movesurface, (
                            round(self.squareSize*j+self.squareSize/6), 
                            round(self.squareSize*i+self.squareSize/6)
                    ))
                # add numbers
                num = self.board[i][j]
                if num != "x" and num != "":
                    movesurface = self.fontBig.render(num, True, self.colorFont)
                    textRect = movesurface.get_rect(center=(j*self.squareSize+self.squareSize//2, i*self.squareSize+self.squareSize//2))
                    self.screen.blit(movesurface, textRect)
        # draw lines
        for i in range(self.dimension+1):
            pygame.draw.line(
                self.screen,
                self.colorLines,
                (round(i*self.squareSize), 0),
                (round(i*self.squareSize), self.boardSize),
                self.lineSize,
            )
            pygame.draw.line(
                self.screen,
                self.colorLines,
                (0, round(i*self.squareSize)),
                (self.boardSize, round(i*self.squareSize)),
                self.lineSize
            )

    def check(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        return True
        
    def setup(self):
        pygame.init()
        screen = self.screen
        self.screen.fill(self.colorBackground)
        pygame.draw.rect(self.screen, self.colorCell, (0, 0, self.boardSize, self.boardSize))
        self.drawBoard()
        # draw buttons
        pygame.draw.rect(screen, self.colorButton, self.buttCheck)
        movesurface = self.fontSmall.render("Check", True, self.colorFont)
        textRect = movesurface.get_rect(center = self.buttCheck.center)
        screen.blit(movesurface, textRect)
        self.updateTimer()
        # draw arrows
        movesurface = self.fontMedium.render("→", True, self.colorFont)
        textRect = movesurface.get_rect(center = (self.outside.width/4 + self.boardSize, self.height//12))
        screen.blit(movesurface, textRect)
        movesurface = self.fontMedium.render("↓", True, self.colorFont)
        textRect = movesurface.get_rect(center = (self.outside.width*3/4 + self.boardSize, self.height//12))
        screen.blit(movesurface, textRect)
        # draw tasks
        for i, task in enumerate(self.horizontalTasks):
            movesurface = self.fontSmall.render(task, True, self.colorFont)
            textRect = movesurface.get_rect(center = (self.outside.width/4 + self.boardSize, self.height*(i+2)//12))
            screen.blit(movesurface, textRect)
        for i, task in enumerate(self.verticalTasks):
            movesurface = self.fontSmall.render(task, True, self.colorFont)
            textRect = movesurface.get_rect(center = (self.outside.width*3/4 + self.boardSize, self.height*(i+2)//12))
            screen.blit(movesurface, textRect)
        
        pygame.display.update()
    # 1 * 100 + 6 * 6 = 137
    # 
    def taskFromNum(self, num):
        if len(num) == 4:
            r = randrange(5)
            if r == 0:
                # plus
                r1 = randrange(999, int(num))
                r2 = int(num) - r1
                return str(r1) + " + " + str(r2)
            else:
                # minus
                r1 = randrange(int(num)+1, 10000)
                r2 = r1 - int(num)
                return str(r1) + " - " + str(r2)
        elif len(num) == 3:
            r = randrange(8)
            if r < 1:
                # division and plus
                num = int(num)
                firstDigit = num//100
                r1 = randrange(1, 10) * 10
                r2 = r1 * (num//r1)
                r3 = num - r2//r1
                return str(r2) + " : " + str(r1) + " + " + str(r3)
            elif r < 5:
                # plus
                r1 = randrange(99, int(num))
                r2 = int(num) - r1
                return str(r1) + " + " + str(r2)
            elif r < 6:
                # mal und plus
                num = int(num)
                firstDigit = num//100
                lastTwoDigits = num%100
                factor = 1
                i = 2
                while i * i <= lastTwoDigits:
                    if i * lastTwoDigits//i == lastTwoDigits:
                        factor = i
                    i += 1
                return str(firstDigit) + " * 100 + " + str(factor) + " * " + str(lastTwoDigits//factor)
            elif r < 7:
                # mal und plus
                r1 = randrange(2, 10) * 10
                r2 = int(num) // r1
                r3 = int(num) - r1*r2
                return str(r3) + " + " + str(r2) + " * " + str(r1)
            else:
                # minus
                r1 = randrange(int(num)+1, 1000)
                r2 = r1 - int(num)
                return str(r1) + " - " + str(r2)
        elif len(num) == 2:
            r = randrange(3)
            if r < 1:
                # minus
                r1 = randrange(int(num)+1, 1000)
                r2 = r1 - int(num)
                return str(r1) + " - " + str(r2)
            elif r < 2:
                num = int(num)
                factor = 1
                i = 2
                while i * i <= num:
                    if i * num//i == num:
                        factor = i
                    i += 1
                return str(factor) + " * " + str(num//factor)
            else:
                r1 = randrange(2, 6)
                r2 = int(num) * r1
                return str(r2) + " : " + str(r1)
        else:
            return "-1"

    def generateTasks(self):
        for hLetter, pos in self.horizontal.items():
            num = ""
            i = 0
            while True:
                try:
                    if self.solution[pos[1]][pos[0]+i] == "x":
                        break
                    num += self.solution[pos[1]][pos[0]+i]
                    i += 1
                except:
                    break
            self.horizontalTasks.append(hLetter + "  " + self.taskFromNum(num))
        for vLetter, pos in self.vertical.items():
            num = ""
            i = 0
            while True:
                try:
                    if self.solution[pos[1]+i][pos[0]] == "x":
                        break
                    num += self.solution[pos[1]+i][pos[0]]
                    i += 1
                except:
                    break
            self.verticalTasks.append(vLetter + "  " + self.taskFromNum(num))

    def play(self):
        self.setup()
        while True:
            self.click()
            self.setup()

if __name__ == "__main__":
    Game().play()