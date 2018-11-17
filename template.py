import pygame
from pygame.locals import *
import time
from random import randint

class Player(object):
    pass

class Designer(object):
    pass

def main():
    # test data structure for maze
    maze = [["" for i in range(10)] for j in range(10)]
    startPoint = (randint(0, 9), randint(0, 9))
    endPoint = (randint(0, 9), randint(0, 9))
    maze[startPoint[0]][startPoint[1]] = "P"
    maze[endPoint[0]][endPoint[1]] = "E"
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 500
    CELL_SIZE = 20
    LINE_SIZE = 2

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

    # Grid lines
    for i in range(1, len(maze)+1):
        # draw horizontal line
        pygame.draw.line(background, (0, 0, 0), [
                         0, i * CELL_SIZE], [len(maze) * CELL_SIZE, i * CELL_SIZE], LINE_SIZE)
        # draw vertical line
        pygame.draw.line(background, (0, 0, 0), [
                         i * CELL_SIZE, 0], [i * CELL_SIZE, len(maze) * CELL_SIZE], LINE_SIZE)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), wall)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
