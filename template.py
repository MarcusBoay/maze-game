import pygame
from pygame.locals import *
import time
from random import randint


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image=None
        self.rect=None
        self.xleftover=0
        self.yleftover=0
        self.placexleftover=0
        self.placeyleftover=0

    def move(self, offsetX, offsetY, grid):
        nextPos = [self.x + offsetX, self.y + offsetY]

        #check for wall and grid bounds
        if (nextPos[0] >= 0 and nextPos[0] < len(grid) and nextPos[1] >= 0 and nextPos[1] < len(grid[0])):
            if (grid[nextPos[0]][nextPos[1]] == "O" or grid[nextPos[0]][nextPos[1]] == "E"):
                grid[self.x][self.y] = "O"
                grid[nextPos[0]][nextPos[1]] == "P"
                self.x = nextPos[0]
                self.y = nextPos[1]

class Game(object):
    def __init__(self):
        pass


def main():
    # test data structure for maze
    rows = 10
    cols = 20
    maze = [["O" for i in range(rows)] for j in range(cols)]
    startPoint = (randint(0, cols - 1), randint(0, rows - 1))
    endPoint = (randint(0, cols - 1), randint(0, rows - 1))
    maze[startPoint[0]][startPoint[1]] = "P"
    maze[endPoint[0]][endPoint[1]] = "E"
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 500
    CELL_SIZE = 20
    LINE_SIZE = 2
    PLAYER_SIZE = 5
    gridOffset = [100,50]

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Basic Pygame program')
    clock = pygame.time.Clock()

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Wall
    wall = pygame.Rect(10, 10, CELL_SIZE, CELL_SIZE)

    # Player Obkect Initialization
    player = Player(startPoint[0], startPoint[1])
    playerXwin = player.x * CELL_SIZE + gridOffset[0] + CELL_SIZE // 2 - PLAYER_SIZE // 2
    playerYwin  = player.y * CELL_SIZE + gridOffset[1] + CELL_SIZE // 2 - PLAYER_SIZE // 2
    player.rect = pygame.Rect(playerXwin, playerYwin, PLAYER_SIZE, PLAYER_SIZE)

    # Grid lines
    for i in range(0, rows + 1):
        # draw horizontal line
        pygame.draw.line(background, (0, 0, 0), [gridOffset[0], gridOffset[1] +
                         (i * CELL_SIZE)], [gridOffset[0]+(cols * CELL_SIZE), gridOffset[1]+ 
                         (i * CELL_SIZE)], LINE_SIZE)
    for i in range(0, cols + 1):
        # draw vertical line
        pygame.draw.line(background, (0, 0, 0), [gridOffset[0]+
                         (i * CELL_SIZE), gridOffset[1]], [gridOffset[0]+ 
                         (i * CELL_SIZE), gridOffset[1]+ (rows * CELL_SIZE)], LINE_SIZE)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if (event.type == QUIT):
                return
            if (event.type == KEYDOWN):
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
                player.move(moveOffset[0], moveOffset[1], maze)
                playerXwin = player.x * CELL_SIZE + gridOffset[0] + CELL_SIZE // 2 - PLAYER_SIZE // 2
                playerYwin  = player.y * CELL_SIZE + gridOffset[1] + CELL_SIZE // 2 - PLAYER_SIZE // 2
                player.rect = pygame.Rect(playerXwin, playerYwin, PLAYER_SIZE, PLAYER_SIZE)
            if event.type == MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                if (click_pos[0] >= gridOffset[0] and click_pos[0] <= (gridOffset[0]+CELL_SIZE*cols) and click_pos[1] >= gridOffset[1] and \
                    click_pos[1] <= (gridOffset[1]+CELL_SIZE*rows)):
                    click_grid = ((click_pos[0]-gridOffset[0])//CELL_SIZE,(click_pos[1]-gridOffset[1])//CELL_SIZE)
                    if (click_grid[0] >= endPoint[0]-1 and click_grid[0] <= endPoint[0]+1) and (click_grid[1] >= endPoint[1]-1 and click_grid[1] <= endPoint[1]+1):
                        pass
                    elif maze[click_grid[0]][click_grid[1]] == "O":
                        maze[click_grid[0]][click_grid[1]] = "W"
                        # and then turn it black
                    elif maze[click_grid[0]][click_grid[1]] == "W":
                        maze[click_grid[0]][click_grid[1]] = "O"
                            # and then make it white


                
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), player.rect)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
