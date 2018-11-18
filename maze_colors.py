import pygame
from pygame.locals import *
import time
from random import randint

def color_change(x, y, maze, offset, CELL_SIZE, screen):
    black = (0,0,0)
    green = (0,255,0)
    red = (255,0,0)
    white = (255,255,255)
    square = Rect((offset[0]+(CELL_SIZE*x)+2), (offset[1]+(CELL_SIZE*y)+2), CELL_SIZE-2, CELL_SIZE-2)
    code = maze[x][y]
    if code == "W":
        screen.fill(black, square)
    if code == "O":
        screen.fill(white, square)
    if code == "E":
        screen.fill(green, square)
    if code == "P":
        screen.fill(red, square)
