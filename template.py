import pygame
from pygame.locals import *
import time
from random import randint
import collections
import pygame.mixer

class Player(object):
    def __init__(self, x, y, dif):
        self.x = x
        self.y = y
        self.rect = None
        self.move_time = 0.0
        self.play_dif = dif

    #Will try to move the player in the grid, return values are (message, hasMoved, previous positions)
    def move(self, offsetX, offsetY, grid):
        nextPos = [self.x + offsetX, self.y + offsetY]
        prevX = self.x
        prevY = self.y

        # check for grid bounds
        if (nextPos[0] >= 0 and nextPos[0] < len(grid) and nextPos[1] >= 0 and nextPos[1] < len(grid[0])) and ((time.time() - self.move_time) >= self.play_dif):
            # check for walls
            if (grid[nextPos[0]][nextPos[1]] == "O"):
                grid[self.x][self.y] = "O"
                grid[nextPos[0]][nextPos[1]] = "P"
                self.x = nextPos[0]
                self.y = nextPos[1]
                return "", True, [prevX, prevY]
            elif (grid[nextPos[0]][nextPos[1]] == "E"):
                grid[self.x][self.y] = "O"
                grid[nextPos[0]][nextPos[1]] = "P"
                self.x = nextPos[0]
                self.y = nextPos[1]
                return "win", True, [prevX, prevY]
            return "found a wall", False, [prevX, prevY]
        else:
            return "found a boundary", False, [prevX, prevY]


class Game(object):
    def __init__(self):
        pygame.init()
        self.rows = 15
        self.cols = 15
        self.maze = [["O" for i in range(self.rows)] for j in range(self.cols)]
        self.startPoint = (randint(0, self.cols - 1), randint(0, self.rows - 1))
        self.endPoint = (randint(0, self.cols - 1), randint(0, self.rows - 1))
        self.maze[self.startPoint[0]][self.startPoint[1]] = "P"
        self.maze[self.endPoint[0]][self.endPoint[1]] = "E"
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 500
        self.CELL_SIZE = 30
        self.LINE_SIZE = 2
        self.PLAYER_SIZE = 5
        self.gridOffset = [350, 30]
        self.background = None
        self.screen = None
        self.clock = None
        self.dSound = pygame.image.load("dSound.png")
        self.eSound = pygame.image.load("eSound.png")
        self.title = pygame.image.load("logo.png")
        self.mode = pygame.image.load("mode.png")
        self.difficulty = pygame.image.load("difficulty.png")
        self.soundMode = True
        self.state = "start"
        self.dif_mode = 0.125
        self.pressure = False
        self.game_clock = 0
        self.pWins = False
        self.diff1 = pygame.image.load("diff1.png")
        self.diff2 = pygame.image.load("diff2.png")
        self.diff3 = pygame.image.load("diff3.png")
        self.diff1Press = pygame.image.load("diff1Press.png")
        self.diff2Press = pygame.image.load("diff2Press.png")
        self.diff3Press = pygame.image.load("diff3Press.png")
        self.noPress = pygame.image.load("noPress.png")
        self.underPress = pygame.image.load("underPressure.png")


    def initializePlayer(self):
        player = Player(self.startPoint[0], self.startPoint[1], self.dif_mode)
        playerXwin = player.x * self.CELL_SIZE + \
            self.gridOffset[0] + self.CELL_SIZE // 2 - self.PLAYER_SIZE // 2
        playerYwin = player.y * self.CELL_SIZE + \
            self.gridOffset[1] + self.CELL_SIZE // 2 - self.PLAYER_SIZE // 2
        player.rect = pygame.Rect(playerXwin, playerYwin, self.PLAYER_SIZE, self.PLAYER_SIZE)
        return player

    def drawGrid(self):
        # Grid lines
        for i in range(0, self.rows + 1):
            # draw horizontal line
            pygame.draw.line(self.background, (0, 0, 0), [self.gridOffset[0], self.gridOffset[1] + (i * self.CELL_SIZE)], [self.gridOffset[0]+(self.cols * self.CELL_SIZE), self.gridOffset[1] + (i * self.CELL_SIZE)], self.LINE_SIZE)
        for i in range(0, self.cols + 1):
            # draw vertical line
            pygame.draw.line(self.background, (0, 0, 0), [self.gridOffset[0] + (i * self.CELL_SIZE), self.gridOffset[1]], [self.gridOffset[0] + (i * self.CELL_SIZE), self.gridOffset[1] + (self.rows * self.CELL_SIZE)], self.LINE_SIZE)

    # Handle behaviour when key pressed, returns message of string data-type
    def handleKeyPress(self, event, player):
        moveOffset = [0, 0]
        if (event.key == K_DOWN):
            moveOffset = [moveOffset[0], moveOffset[1] + 1]
        if (event.key == K_UP):
            moveOffset = [moveOffset[0], moveOffset[1] - 1]
        if (event.key == K_RIGHT):
            moveOffset = [moveOffset[0] + 1, moveOffset[1]]
        if (event.key == K_LEFT):
            moveOffset = [moveOffset[0] - 1, moveOffset[1]]
        # TODO: check if player can reach exit
        message, hasMoved, prevPlayerPos = player.move(moveOffset[0], moveOffset[1], self.maze)
        playerXwin = player.x * self.CELL_SIZE + \
            self.gridOffset[0] + self.CELL_SIZE // 2 - self.PLAYER_SIZE // 2
        playerYwin = player.y * self.CELL_SIZE + \
            self.gridOffset[1] + self.CELL_SIZE // 2 - self.PLAYER_SIZE // 2
        player.rect = pygame.Rect(playerXwin, playerYwin, self.PLAYER_SIZE, self.PLAYER_SIZE)
        if (hasMoved):
            player.move_time = time.time()
            if message == "win":
                self.pWins = True
                self.state = "end"
            if (self.soundMode):            
                self.c_step.play(self.s_step)
            self.color_change(prevPlayerPos[0], prevPlayerPos[1])
        else:
            if (self.soundMode):
                self.c_wall_hit.play(self.s_wall_hit)
        self.color_change(player.x, player.y)

        return message

    # Handle behaviour when mouse button pressed in window, returns message of string data-type
    def handleMousePress(self, player):
        click_pos = pygame.mouse.get_pos()
        if (click_pos[0] >= self.gridOffset[0] and click_pos[0] <= (self.gridOffset[0]+self.CELL_SIZE*self.cols) and click_pos[1] >= self.gridOffset[1] and click_pos[1] <= (self.gridOffset[1]+ self.CELL_SIZE*self.rows)):
            click_grid = ((click_pos[0]-self.gridOffset[0])//self.CELL_SIZE,     (click_pos[1]-self.gridOffset[1])//self.CELL_SIZE)
            validPathBool = self.hasValidPath(player)
            if (click_grid[0] >= self.endPoint[0]-1 and click_grid[0] <= self.endPoint[0]+1) and (click_grid[1] >= self.endPoint[1]-1 and click_grid[1] <= self.endPoint[1]+1):
                if (self.soundMode):
                    self.c_wrong.play(self.s_wrong)
                return "forbidden area"
            elif self.maze[click_grid[0]][click_grid[1]] == "P":
                if (self.soundMode):
                    self.c_click_on_player.play(self.s_click_on_player)
                return "clicked on player"
            elif (self.maze[click_grid[0]][click_grid[1]] == "O"):
                self.maze[click_grid[0]][click_grid[1]] = "W"
                validPathBool = self.hasValidPath(player)
                if (validPathBool is False):
                    self.maze[click_grid[0]][click_grid[1]] = "O"
                    if (self.soundMode):
                        self.c_wrong.play(self.s_wrong)
                    return "NO VALID PATH"
                if (self.soundMode):
                    self.c_wall_build.play(self.s_wall_build)
                self.color_change(click_grid[0], click_grid[1])
                # and then turn it black
                return ""
            elif self.maze[click_grid[0]][click_grid[1]] == "W":
                self.maze[click_grid[0]][click_grid[1]] = "O"
                self.color_change(click_grid[0], click_grid[1])
                if (self.soundMode):
                    self.c_wall_build.play(self.s_wall_build)
                # and then make it white
                return ""
        elif (click_pos[0] > 135 and click_pos[0] < 195 and click_pos[1] > 420 and click_pos[1] < 480):
            self.soundMode = not self.soundMode
            return "toggled sound"
        else:
            return "click outside grid"

    def eventLoop(self):
        self.maze = [["O" for i in range(self.rows)] for j in range(self.cols)]
        self.startPoint = (randint(0, self.cols - 1), randint(0, self.rows - 1))
        self.endPoint = (randint(0, self.cols - 1), randint(0, self.rows - 1))
        self.maze[self.startPoint[0]][self.startPoint[1]] = "P"
        self.maze[self.endPoint[0]][self.endPoint[1]] = "E"
        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))
        player = self.initializePlayer()
        self.initializeSound()

        self.drawGrid()
        self.color_change(self.endPoint[0],self.endPoint[1])
        self.color_change(player.x, player.y)
        self.color_change(self.endPoint[0],self.endPoint[1])
        self.color_change(player.x, player.y)

        # Blit everything to the screen
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, (0,0))
        self.screen.blit(self.mode,(30,200))
        self.screen.blit(self.difficulty,(30,290))
        self.screen.blit(self.eSound,(135,420))
        pygame.display.flip()
        message = ""
        clock_font = pygame.font.SysFont("futura",30)
        if self.pressure:
            
            self.game_clock = time.time()
            if self.dif_mode == 0.125:
                timer = 20
            if self.dif_mode == 0.15:
                timer = 15
            if self.dif_mode == 0.1:
                timer = 24
            clock_text = clock_font.render("15", 0, [0,0,0])
            # self.screen.blit(clock_text, (900,150))
        pygame.display.flip()
        while self.state == "game":
            if (time.time() - self.game_clock >= 15) and self.pressure:
                self.state = "end"
                continue
            elif self.pressure:
                if (15 - (time.time() - self.game_clock)) != timer:
                    timer = (15 - (time.time() - self.game_clock))
                    clock_text = clock_font.render("%d" % timer, 0, [0,0,0])
                    self.screen.blit(clock_text, (900,150))
                    pygame.display.flip()
            elif not self.pressure:
                clock_text = clock_font.render("inf.", 0, [0,0,0])
            for event in pygame.event.get():
                if (event.type == QUIT):
                    self.state = "quit"
                    return
                if (event.type == KEYDOWN):
                    message = self.handleKeyPress(event, player)
                if event.type == MOUSEBUTTONDOWN:
                    message = self.handleMousePress(player)

                if message != "":
                    print (message)
            timer = (15 - (time.time() - self.game_clock))
            if self.pressure:
                self.screen.blit(clock_text, (900,150))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title, (0,0))
            self.screen.blit(self.mode,(30,200))
            self.screen.blit(self.difficulty,(30,290))
            pygame.draw.rect(self.screen, (0, 0, 0), player.rect)
            self.screen.blit(clock_text, (900,150))
            if self.soundMode:
                self.screen.blit(self.eSound,(135,420))
            else:
                self.screen.blit(self.dSound,(135,420))
            pygame.display.flip()
            self.clock.tick(60)

    # Searches for a valid path from player to end point, returns a bool indicating existence of a valid path
    def hasValidPath(self, player):
        visitedGrid = [[0 for i in range(self.rows)] for j in range(self.cols)]
        queue = collections.deque([[player.x, player.y]])

        while (queue):
            curPos = queue.popleft()
            visitedGrid[curPos[0]][curPos[1]] = 1

            #check if exit has been searched
            if (visitedGrid[self.endPoint[0]][self.endPoint[1]] == 1):
                return True

            #add 4 directions from current position
            if (curPos[0] - 1 >= 0 and self.maze[curPos[0] - 1][curPos[1]] != "W" and visitedGrid[curPos[0] - 1][curPos[1]] == 0):
                queue.append([curPos[0] - 1, curPos[1]])
                visitedGrid[curPos[0] - 1][curPos[1]] = 1
            if (curPos[0] + 1 < self.cols and self.maze[curPos[0] + 1][curPos[1]] != "W"  and visitedGrid[curPos[0] + 1][curPos[1]] == 0):
                queue.append([curPos[0] + 1, curPos[1]])
                visitedGrid[curPos[0] + 1][curPos[1]] = 1
            if (curPos[1] - 1 >= 0 and self.maze[curPos[0]][curPos[1] - 1] != "W" and visitedGrid[curPos[0]][curPos[1] - 1] == 0):
                queue.append([curPos[0], curPos[1] - 1])
                visitedGrid[curPos[0]][curPos[1] - 1] = 1
            if (curPos[1] + 1 < self.rows and self.maze[curPos[0]][curPos[1] + 1] != "W" and visitedGrid[curPos[0]][curPos[1] + 1] == 0):
                queue.append([curPos[0], curPos[1] + 1])
                visitedGrid[curPos[0]][curPos[1] + 1] = 1

        #no valid path found
        return False
                

    def main(self):
         # Initialise screen
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Basic Pygame program')
        self.clock = pygame.time.Clock()
        pygame.mixer.init() 

        while 1:
            if self.state == "start":
                self.startLoop()
            elif self.state == "game":
                self.eventLoop()
            elif self.state == "end":
                self.endLoop()
            elif self.state == "quit":
                return
    
    def color_change(self, x, y):
        black = (0, 0, 0)
        green = (54, 159, 217)
        red = (237, 17, 104)
        white = (255, 255, 255)
        square = pygame.Rect((self.gridOffset[0]+(self.CELL_SIZE*x)+2),
                    (self.gridOffset[1]+(self.CELL_SIZE*y)+2), self.CELL_SIZE-2, self.CELL_SIZE-2)
        code = self.maze[x][y]

        if code == "W":
            pygame.draw.rect(self.background, black, square, 0)
        if code == "O":
            pygame.draw.rect(self.background, white, square, 0)
        if code == "E":
            pygame.draw.rect(self.background, green, square, 0)
        if code == "P":
            pygame.draw.rect(self.background, red, square, 0)


    def initializeSound(self):
        self.s_wall_hit = pygame.mixer.Sound('wall_hit.wav')
        self.s_click_on_player = pygame.mixer.Sound('click_on_player.wav')
        self.s_step = pygame.mixer.Sound('step.wav')
        self.s_wall_build = pygame.mixer.Sound('wall_build.wav')
        self.s_wrong = pygame.mixer.Sound('wrong.wav')
        self.c_wall_hit = pygame.mixer.Channel(0)
        self.c_click_on_player = pygame.mixer.Channel(1)
        self.c_step = pygame.mixer.Channel(2)
        self.c_wall_build = pygame.mixer.Channel(3)
        self.c_wrong = pygame.mixer.Channel(4)

    def startLoop(self):
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))
        self.screen.blit(self.background, (0, 0))

        start_font = pygame.font.SysFont("timesnewroman", 20)

        name_text = start_font.render("A game by Rafaella Grandma, Keven Smelly, and Marcus BOYEEEEEEE", 0, [0,0,0])
        self.screen.blit(self.title,(500-(350/2),50))
        if self.dif_mode == 1:
            self.screen.blit(self.diff1Press,(300,270))
            self.screen.blit(self.diff2,(440,270))
            self.screen.blit(self.diff3,(580,270))
        elif self.dif_mode == 2:
            self.screen.blit(self.diff1,(300,270))
            self.screen.blit(self.diff2Press,(440,270))
            self.screen.blit(self.diff3,(580,270))
        elif self.dif_mode == 3:
            self.screen.blit(self.diff1,(300,270))
            self.screen.blit(self.diff2,(440,270))
            self.screen.blit(self.diff3Press,(580,270))
        if self.pressure:
            self.screen.blit(self.underPress,(440,360))
        else:
            self.screen.blit(self.noPress,(440,360))
        self.screen.blit(name_text, (260,230))
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if (event.type == QUIT):
                    self.state = "quit"
                    return
                if (event.type == KEYDOWN):
                    if event.key == K_1:
                        self.dif_mode = 0.10
                    elif event.key == K_2:
                        self.dif_mode = 0.125
                    elif event.key == K_3:
                        self.dif_mode = 0.15
                    elif event.key == K_s:
                        self.state = "game"
                        return
                if (event.type == MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                    if pos[0]> 440 and pos[0]< 560 and pos[1] >360 and pos[1]<436:
                        self.pressure = not self.pressure
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title,(500-(350/2),50))
            if self.dif_mode == 0.10:
                self.screen.blit(self.diff1Press,(300,270))
                self.screen.blit(self.diff2,(440,270))
                self.screen.blit(self.diff3,(580,270))
            elif self.dif_mode == 0.125:
                self.screen.blit(self.diff1,(300,270))
                self.screen.blit(self.diff2Press,(440,270))
                self.screen.blit(self.diff3,(580,270))
            elif self.dif_mode == 0.15:
                self.screen.blit(self.diff1,(300,270))
                self.screen.blit(self.diff2,(440,270))
                self.screen.blit(self.diff3Press,(580,270))
            if self.pressure:
                self.screen.blit(self.underPress,(440,360))
            else:
                self.screen.blit(self.noPress,(440,360))
            self.screen.blit(name_text, (260,230))
            pygame.display.flip()


    def endLoop(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255,255,255))
        if self.pWins:
            self.endScene = pygame.image.load("pWins.png")
        else:
            self.endScene = pygame.image.load("dWins.png")
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.endScene, (0, 0))
        if self.soundMode:
            self.screen.blit(self.eSound,(135,420))
        else:
            self.screen.blit(self.dSound,(135,420))
        
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if (event.type == QUIT):
                    self.state = "quit"
                    return
                if (event.type == MOUSEBUTTONDOWN):
                    self.endMousePress()
                    return

    def endMousePress(self):
        self.state = "start"

def main():
    game = Game()
    game.main()


if __name__ == '__main__':
    main()
