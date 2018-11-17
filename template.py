import pygame
from pygame.locals import *
import time
from random import randint


class Player():
    def __init__(self, max_x, max_y):
        self.x = randint(0, max_x - 1)
        self.y = randint(0, max_y - 1)


class Designer(object):
    pass


def main():
    # test data structure for maze
    MAZE_SIZE = 10
    PLAYER_SIZE = 5
    maze = [["" for i in range(MAZE_SIZE)] for j in range(MAZE_SIZE)]
    player = Player(MAZE_SIZE, MAZE_SIZE)
    endPoint = (randint(0, 9), randint(0, 9))
    maze[player.x][player.y] = "P"
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
        # Player
        playerModel = pygame.Rect(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)

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
                playerModel.move_ip(moveOffset[0] * CELL_SIZE, moveOffset[1] * CELL_SIZE)

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), playerModel)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
