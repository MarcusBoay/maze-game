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

def maze_update():
    # Mouse click = turn it black
    # Player move = turn old player pos white, turn new player pos red
    # Make maze end = green colour
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "P":
                # make this grid square show up as red
                pass
            if maze[i][j] == "E":
                #make this grid square show up as green
                pass
            if maze[i][j] == "W":
                # make this grid square show up as black
                pass
            if maze[i][j] == "O":
                # make this grid square show up as white
                pass

class Designer(object):
    pass


def main():
    # test data structure for maze
    rows = 10
    cols = 20
    maze = [["" for i in range(rows)] for j in range(cols)]
    startPoint = (randint(0, cols - 1), randint(0, rows - 1))
    endPoint = (randint(0, cols - 1), randint(0, rows - 1))
    maze[startPoint[0]][startPoint[1]] = "P"
    maze[endPoint[0]][endPoint[1]] = "E"
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 500
    CELL_SIZE = 20
    LINE_SIZE = 2
    PLAYER_SIZE = 5
    startpoint = [100,50]

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

    # Player
    player = Player(startPoint[0], startPoint[1])
    player.rect = pygame.Rect(player.x * CELL_SIZE + startpoint[0] + CELL_SIZE // 2 - PLAYER_SIZE // 2, player.y * CELL_SIZE + startpoint[1] + CELL_SIZE // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)

    # Grid lines
    for i in range(0, rows + 1):
        # draw horizontal line
        pygame.draw.line(background, (0, 0, 0), [startpoint[0], startpoint[1] +
                         (i * CELL_SIZE)], [startpoint[0]+(cols * CELL_SIZE), startpoint[1]+ 
                         (i * CELL_SIZE)], LINE_SIZE)
    for i in range(0, cols + 1):
        # draw vertical line
        pygame.draw.line(background, (0, 0, 0), [startpoint[0]+
                         (i * CELL_SIZE), startpoint[1]], [startpoint[0]+ 
                         (i * CELL_SIZE), startpoint[1]+ (rows * CELL_SIZE)], LINE_SIZE)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                curPos = [player.x, player.y]
                nextPos = [player.x, player.y]
                moveOffset = [0, 0]
                if (event.key == K_DOWN):
                    nextPos = [nextPos[0], nextPos[1] + 1]
                    moveOffset = [moveOffset[0], moveOffset[1] + 1]
                if (event.key == K_UP):
                    nextPos = [nextPos[0], nextPos[1] - 1]
                    moveOffset = [moveOffset[0], moveOffset[1] - 1]
                if (event.key == K_RIGHT):
                    nextPos = [nextPos[0] + 1, nextPos[1]]
                    moveOffset = [moveOffset[0] + 1, moveOffset[1]]
                if (event.key == K_LEFT):
                    nextPos = [nextPos[0] - 1, nextPos[1]]
                    moveOffset = [moveOffset[0] - 1, moveOffset[1]]

                # TODO: check if collide with wall
                # TODO: check if out of bounds
                # TODO: check if player can reach exit

                player.x = nextPos[0]
                player.y = nextPos[1]
                player.rect.move_ip(moveOffset[0] * CELL_SIZE, moveOffset[1] * CELL_SIZE)

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), player.rect)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
