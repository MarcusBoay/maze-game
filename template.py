import pygame
from pygame.locals import *
import time
from random import randint


def main():
    # test data structure for maze
    maze = [["" for i in range(10)] for j in range(10)]
    startPoint = (randint(0, 9), randint(0, 9))
    endPoint = (randint(0, 9), randint(0, 9))
    maze[startPoint[0]][startPoint[1]] = "P"
    maze[endPoint[0]][endPoint[1]] = "E"

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption('Basic Pygame program')
    clock = pygame.time.Clock()

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Wall
    wall = pygame.Rect(10, 10, 10, 10)

    # Grid lines
    

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)

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
        wall.move_ip(1, 1)


if __name__ == '__main__':
    main()
