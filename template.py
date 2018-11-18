import pygame
from pygame.locals import *
import time
from random import randint

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = None
        self.rect = None
        self.xleftover = 0
        self.yleftover = 0
        self.placexleftover = 0
        self.placeyleftover = 0

    def move(self, offsetX, offsetY, grid):
        nextPos = [self.x + offsetX, self.y + offsetY]

        # check for grid bounds
        if (nextPos[0] >= 0 and nextPos[0] < len(grid) and nextPos[1] >= 0 and nextPos[1] < len(grid[0])):
            # check for walls
            if (grid[nextPos[0]][nextPos[1]] == "O" or grid[nextPos[0]][nextPos[1]] == "E"):
                grid[self.x][self.y] = "O"
                grid[nextPos[0]][nextPos[1]] == "P"
                self.x = nextPos[0]
                self.y = nextPos[1]
                return ""
            return "found a wall"
        else:
            return "found a boundary"


class Game(object):
    def __init__(self):
        self.rows = 15
        self.cols = 20
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

    def initializePlayer(self):
        player = Player(self.startPoint[0], self.startPoint[1])
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
        message = player.move(moveOffset[0], moveOffset[1], self.maze)
        playerXwin = player.x * self.CELL_SIZE + \
            self.gridOffset[0] + self.CELL_SIZE // 2 - self.PLAYER_SIZE // 2
        playerYwin = player.y * self.CELL_SIZE + \
            self.gridOffset[1] + self.CELL_SIZE // 2 - self.PLAYER_SIZE // 2
        player.rect = pygame.Rect(playerXwin, playerYwin, self.PLAYER_SIZE, self.PLAYER_SIZE)

        return message

    # Handle behaviour when mouse button pressed in window, returns message of string data-type
    def handleMousePress(self):
        click_pos = pygame.mouse.get_pos()
        if (click_pos[0] >= self.gridOffset[0] and click_pos[0] <= (self.gridOffset[0]+self.CELL_SIZE*self.cols) and click_pos[1] >= self.gridOffset[1] and click_pos[1] <= (self.gridOffset[1]+ self.CELL_SIZE*self.rows)):
            click_grid = ((click_pos[0]-self.gridOffset[0])//self.CELL_SIZE,     (click_pos[1]-self.gridOffset[1])//self.CELL_SIZE)
            if (click_grid[0] >= self.endPoint[0]-1 and click_grid[0] <= self.endPoint[0]+1) and (click_grid[1] >= self.endPoint[1]-1 and click_grid[1] <= self.endPoint[1]+1):
                return "forbidden area"
            elif self.maze[click_grid[0]][click_grid[1]] == "P":
                return "clicked on player"
            elif self.maze[click_grid[0]][click_grid[1]] == "O":
                self.maze[click_grid[0]][click_grid[1]] = "W"
                # and then turn it black
                return ""
            elif self.maze[click_grid[0]][click_grid[1]] == "W":
                self.maze[click_grid[0]][click_grid[1]] = "O"
                # and then make it white
                return ""
            else:
                return "click outside grid"

    def eventLoop(self, player):
        message = ""
        while 1:
            for event in pygame.event.get():
                if (event.type == QUIT):
                    return
                if (event.type == KEYDOWN):
                    message = self.handleKeyPress(event, player)
                if event.type == MOUSEBUTTONDOWN:
                    message = self.handleMousePress()

                if message != "":
                    print (message)

            self.screen.blit(self.background, (0, 0))
            pygame.draw.rect(self.screen, (0, 0, 0), player.rect)
            pygame.display.flip()
            self.clock.tick(60)

    def main(self):
         # Initialise screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Basic Pygame program')
        self.clock = pygame.time.Clock()

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

        # Wall
        wall = pygame.Rect(10, 10, self.CELL_SIZE, self.CELL_SIZE)

        # Player Object Initialization
        player = self.initializePlayer()

        self.drawGrid()

        # Blit everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # Event loop
        self.eventLoop(player)
    
    def color_change(self, x, y, maze, offset, CELL_SIZE, screen):
        black = (0, 0, 0)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        square = pygame.Rect((offset[0]+(self.CELL_SIZE*x)+2),
                    (offset[1]+(self.CELL_SIZE*y)+2), self.CELL_SIZE-2, self.CELL_SIZE-2)
        code = self.maze[x][y]
        if code == "W":
            screen.fill(black, square)
        if code == "O":
            screen.fill(white, square)
        if code == "E":
            screen.fill(green, square)
        if code == "P":
            screen.fill(red, square)


def main():
    game = Game()
    game.main()


if __name__ == '__main__':
    main()
